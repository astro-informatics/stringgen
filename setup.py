from pathlib import Path
from setuptools import find_packages, setup

this_directory = Path(__file__).parent


long_description = (this_directory / ".pip_readme.md").read_text()
requirements = (this_directory / "requirements.txt").read_text().split("\n")


setup(
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
    ],
    name="stringgen",
    version="0.0.1",
    url="https://github.com/astro-informatics/stringgen",
    author="Matthew Price, Matthijs Mars, Matthew Docherty, Alessio Spurio Mancini, Auggie Marignier, Jason McEwen",
    license="MIT",
    python_requires=">=3.8",
    install_requires=requirements,
    description="Fast emulation of cosmic string anisotropies",
    long_description_content_type="text/x-rst",
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "stringgen.data": [
            "features_Price_et_al_2022.pkl",
        ],
    },
)
