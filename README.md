[![image](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![image](http://img.shields.io/badge/arXiv-xxxx.xxxxx-orange.svg?style=flat)](https://arxiv.org/abs/xxxx.xxxxx)<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-6-orange.svg?style=flat-square)](#contributors-) <!-- ALL-CONTRIBUTORS-BADGE:END --> 
[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Scattering based cosmic string emulation

`stringgen` is a tool for creating emulations of cosmic string maps with similar statistics to based on the works in Price et al. 2022 (in prep.). It uses wavelet phase harmonics to calculate scattering coefficients of the simulations. These coefficients can then be used to synthesize new realisations which have similar statistics to the original simulations. 

## Quick install :computer:
You can install `stringgen` using PyPi by running 
```bash
pip install stringgen
```

## Install from source :computer:
Alternative you can install the code from source by cloning and installing manually:

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
   AUTHOR      = "Matthew A. Price and Matthijs Mars and Jason D. McEwen and Contributors",
   TITLE       = "TBA",
   YEAR        = "2023",
   EPRINT      = "arXiv:0000.00000"        
}
```

## License :memo:

We provide this code under an MIT open-source licence with the hope that
it will be of use to a wider community.

Copyright 2023 Matthijs Mars, Matthew Price, Jason McEwen and contributors.

`stringgen` is free software made available under the MIT License. For
details see the LICENSE file.
