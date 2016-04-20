from setuptools import setup
from kegg.version import __version__

setup(
    name="kg",
    packages=["kegg"],
    scripts=["bin/kg"],
    version=__version__,
    description="Access KEGG from the command line.",
    author="Endre Bakken Stovner",
    author_email="endrebak@stud.ntnu.no",
    url="http://github.com/endrebak/kg",
    keywords=["KEGG", "Kyoto Encyclopedia of Genes and Genomes"],
    license=["GPL-3.0"],
    install_requires=["pandas>=0.16", "biopython>=1.65", "ebs>=0.0.10",
                      "docopt", "joblib"],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Other Environment", "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Scientific/Engineering"
    ],
    long_description=("Access (a subset of) the Kyoto Encyclopedia of Genes\n"
                      "and Genomes from the command line or Python."
                      "See the URL for examples and docs."))
