import time
import torch
import tqdm

import numpy as np
import scipy.optimize as opt
import pywph as pw


class CosmicStringEmulator:
    def __init__(
        self,
        emulation_shape=(1024, 1024),
        J=9,
        L=9,
        dn=5,
        norm="auto",
        pbc=True,
        cplx=False,
        device=None,
    ):
        self.emulation_shape = emulation_shape
        self.norm = norm  # Normalization
        self.pbc = pbc  # Periodic boundary conditions
        if device is None:
            self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device  # Torch device to use for the emulation

        # create wavelet phase harmonic operator
        self.wph_op = pw.WPHOp(
            emulation_shape[0],
            emulation_shape[1],
            J=J,
            L=L,
            dn=dn,
            device=device,
            cplx=cplx,
        )

    @staticmethod
    def download_features():
        r"""Downloads the features used in Price et al. 2022 [1]_

        Returns
        -------
        features: list
            A list of 300 features for cosmic string emulation containing, image means and standard deviations, scattering coefficients, scattering normalisation constants

        References
        -------
        .. [1] Price et al. 2022 (in prep.)
        """
        raise NotImplemented

    def generate_features(self, input_images):
        r"""For each image, calculates the scattering coefficients, the corresponding normalisation constants, and image mean and standard deviation, which are used for emulation. 

        Parameters
        ----------
        input_images : array_like
            Array of input images which will be used to calculate scattering coefficients, to be used in emulation. 

        Returns
        -------
        features: list
            A list of features for emulation, one set of features for every input image provided. Each element of the list contains a list with: image mean, image standard deviation, scattering coefficients, normalisation constants
        
        Examples
        --------
        
        >>> from cosmic_string_emulator import CosmicStringEmulator
        >>> cosmicStringEmulator = CosmicStringEmulator()
        >>> input_images = np.random.rand(10, 1024, 1024)
        >>> features = cosmicStringEmulator.generate_features(input_images)
        """
        assert input_images.shape[-2:] == self.emulation_shape
        assert input_images.ndim == 3

        # initialising lists
        im_means, im_stds, wph_coeffs = (list() for i in range(3))
        wph_means, wph_stds, sm_means_1, sm_means_2, sm_stds = (
            list() for i in range(5)
        )

        for i in tqdm.tqdm(
            range(len(input_images)), desc="Calculating wph coefficients"
        ):
            mean = np.nanmean(input_images[i])
            std = np.nanstd(input_images[i])

            standardised_image = (input_images[i] - mean) / std

            im_means.append(mean)
            im_stds.append(std)

            # make sure normalisation is cleared before scattering next image
            self.wph_op.clear_normalization()

            # Calculating scattering coefficients and saving them
            a_coeffs = self.wph_op.apply(standardised_image, norm="auto", pbc=True)
            wph_coeffs.append(np.squeeze(a_coeffs.cpu().detach().numpy()))

            del a_coeffs  # delete tensor to clear out device memory

            # Save normalisation constants of the wph operator
            normalisation = self.wph_op.get_normalization()

            wph_means.append(normalisation[0].detach().cpu().numpy())
            wph_stds.append(normalisation[1].detach().cpu().numpy())
            sm_means_1.append(normalisation[2].detach().cpu().numpy())
            sm_means_2.append(normalisation[3].detach().cpu().numpy())
            sm_stds.append(normalisation[4].detach().cpu().numpy())

            del normalisation

        normalisation_constants = list(
            zip(wph_means, wph_stds, sm_means_1, sm_means_2, sm_stds)
        )

        # save in list as for every input: mean, std, wph coefficients, normalisation coefficients
        features = list(zip(im_means, im_stds, wph_coeffs, normalisation_constants))

        return features

    def emulate(self, features, n_emulations=1, max_iterations=100):
        r"""Emulates `n_emulations` images matching the statistics of one of the features provided. Picks a random target from the list of features as emulation target.

        Parameters
        ----------
        features : list
            List of features for emulation created by `CosmicStringEmulator.calculate_features()` or `CosmicStringEmulator.download_features()`
        max_iter : int
            The maximum amount of iterations in the optimisation scheme. (Defaults to 100)

        Returns
        -------
        emulation: array
            A 2D emulated image matching the statistics of a randomly selected target from the set of input features . 
        
        Examples
        --------
        This function can be used to create random emulations of 2D cosmic strings simulations similar to Price et al. 2022:
        
        >>> from cosmic_string_emulator import CosmicStringEmulator
        >>> cosmicStringEmulator = CosmicStringEmulator()
        >>> features = cosmicStringEmulator.download_features()
        >>> emulation = cosmicStringEmulator.generate_features(features)   

        Alternatively, the code can be used to generate your own target features and emulate matching images for those:
        
        >>> from cosmic_string_emulator import CosmicStringEmulator
        >>> cosmicStringEmulator = CosmicStringEmulator()
        >>> input_images = np.random.rand(10, 1024, 1024)
        >>> features = cosmicStringEmulator.generate_features(input_images)
        >>> emulation = cosmicStringEmulator.generate_features(features)
        """
        emulations = []
        optim_params = {
            "maxiter": max_iterations,
            "gtol": 1e-14,
            "ftol": 1e-14,
            "maxcor": 50,
        }

        for n in range(n_emulations):
            print(f"=== Emulation {n} out of {n_emulations} ===")
            # randomly pick one target from features
            random_target = np.random.randint(0, len(features))
            mean, std, wph_coeffs, normalisation_constants = features[random_target]

            # adjusting normalisation for selected target
            self.wph_op.clear_normalization()
            tensor_norms = []
            for k in normalisation_constants:
                tensor_norms.append(torch.from_numpy(k).to(self.device))

            self.wph_op.set_normalization(*tensor_norms)
            del tensor_norms

            # initialise random starting image with mean=0, std=1
            x0 = np.random.normal(0, 1, self.emulation_shape)
            coeffs = torch.from_numpy(wph_coeffs).to(self.device).contiguous()

            # synthesis
            def objective(x):
                start_time = time.time()
                # Reshape x
                x_curr = x.reshape((self.emulation_shape))
                # Compute the loss (squared 2-norm)
                loss_tot = torch.zeros(1)
                x_curr, nb_chunks = self.wph_op.preconfigure(
                    x_curr, requires_grad=True, pbc=self.pbc
                )
                for i in range(nb_chunks):
                    coeffs_chunk, indices = self.wph_op.apply(
                        x_curr, i, norm=self.norm, ret_indices=True, pbc=self.pbc
                    )
                    loss = torch.sum(torch.abs(coeffs_chunk - coeffs[indices]) ** 2)
                    loss.backward(retain_graph=True)
                    loss_tot += loss.detach().cpu()
                    del coeffs_chunk, indices, loss
                # Reshape the gradient
                x_grad = x_curr.grad.cpu().numpy().astype(x.dtype)
                print(
                    f"Loss: {loss_tot.item()} (computed in {time.time() - start_time}s)"
                )
                return loss_tot.item(), x_grad.ravel()

            total_start_time = time.time()
            result = opt.minimize(
                objective,
                x0.ravel(),
                method="L-BFGS-B",
                jac=True,
                tol=None,
                options=optim_params,
            )
            final_loss, x_final, niter, msg = (
                result["fun"],
                result["x"],
                result["nit"],
                result["message"],
            )
            print(
                f"Synthesis ended in {niter} iterations with optimizer message: {msg}"
            )
            print(f"Synthesis time: {time.time() - total_start_time}s")

            x_final = x_final.reshape(self.emulation_shape).astype(np.float32)
            x_final = x_final * std + mean
            emulations.append(x_final)
        return np.array(emulations).reshape(
            n_emulations, self.emulation_shape[0], self.emulation_shape[1]
        )
