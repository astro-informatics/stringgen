
import numpy as np

from cosmic_string_emulator import CosmicStringEmulator

def test_cse():
    """Tests a very simple/small emulation case to see whether all functions run through without any issues. 
    """
    emulator = CosmicStringEmulator(
        emulation_shape=(32, 32),
        J=4,
        L=4,
        dn=1,
        norm="auto",
        pbc=True,
        cplx=False,
    )

    im = np.random.rand(1,32,32)
    features = emulator.generate_features(im)
    emulation = emulator.emulate(features, n_emulations=1, max_iterations=3)
