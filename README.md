[![image](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![image](http://img.shields.io/badge/arXiv-2307.04798-orange.svg?style=flat)](https://arxiv.org/abs/2307.04798)<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-6-orange.svg?style=flat-square)](#contributors-) <!-- ALL-CONTRIBUTORS-BADGE:END --> 
[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Scattering based cosmic string emulation

`stringgen` is a tool for creating emulations of cosmic string maps with statistics similar to those of a single (or small ensemble) of reference simulations. It uses wavelet phase harmonics to calculate a compressed representation of these reference simulations, which may then be used to synthesize new realisations with accurate statistical properties, e.g. 2 and 3 point correlations, skewness, kurtosis, and Minkowski functionals.

## Install from source :computer:
One may install the code from source by cloning and installing manually:

```
git clone https://github.com/astro-informatics/stringgen.git
cd stringgen
bash build_stringgen.sh
```

## Usage :rocket:

To generate your own cosmic string maps `stringgen` is as simple follows:

``` python
from stringgen import CosmicStringEmulator

# Configure the emulator
emulator = CosmicStringEmulator(
        emulation_shape=(1024, 1024),   # Shape of image
        J=9,                        # Number of wavelet scales
        L=9                         # Number of directions
    )

# Load latent data-bank
features = emulator.get_features()

# Generate n_emulation=1 synthetic cosmic string maps
emulation = emulator.emulate(features, n_emulations=1)
```

## Contributors ✨

Thanks goes to these wonderful people ([emoji
key](https://allcontributors.org/docs/en/emoji-key)):
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

## Attribution :books: 
Should this code be used in any way, we kindly request that the following article is
referenced. A BibTeX entry for this reference may look like:

``` 
@article{price:stringgen, 
   AUTHOR      = "Matthew A. Price, Matthijs Mars, Matthew M. Docherty, Alessio Spurio Mancini, Augustin Marignier, Jason. D. McEwen",
   TITLE       = "Fast emulation of anisotropies induced in the cosmic microwave background by cosmic strings",
   YEAR        = "2023",
   JOURNAL     = "The Open Journal of Astrophysics,
   DOI         = "10.21105/astro.2307.04798",
   EPRINT      = "arXiv:2307.04798"        
}
```

## License :memo:

We provide this code under an MIT open-source licence with the hope that
it will be of use to a wider community.

Copyright 2023 Matthijs Mars, Matthew Price, Jason McEwen and contributors.

`stringgen` is free software made available under the MIT License. For
details see the LICENSE file.
