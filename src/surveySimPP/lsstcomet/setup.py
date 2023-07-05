#!/usr/bin/env python
from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name="lsstcomet",
        version="0.1.0",
        description="Template comet models for LSST.",
        author="Michael S. P. Kelley",
        author_email="msk@astro.umd.edu",
        url="https://github.com/lsst-sssc/lsstcomet",
        packages=find_packages(),
        package_data={"lsstcomet": "tests/*.dat"},
        requires=["numpy"],
        setup_requires=["pytest-runner"],
        tests_require=["pytest", "astropy", "sbpy", "synphot"],
        license="MIT",
    )
