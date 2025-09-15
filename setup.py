#!/usr/bin/env/python

from setuptools import setup, find_packages
import os

if __name__ == "__main__":
    with open("README.md", "r") as fh:
        long_description = fh.read()

#    VERSION = os.getenv("GITHUB_PROGRAM_VERSION")
#    if not VERSION:
#        raise ValueError("Did not receive version info from GitHub")

    setup(
        name="core-aprs-client",
#        version=VERSION,
        version="0.0.1",
        description="Core APRS Client framework",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Joerg Schultze-Lutter",
        author_email="joerg.schultze.lutter@gmail.com",
        url="https://github.com/joergschultzelutter/core-aprs-client",
        packages=find_packages(),
        include_package_data=True,
        classifiers=[
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Natural Language :: English",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: OS Independent",
            "Development Status :: 4 - Beta",
            "Topic :: Software Development",
            "Topic :: Communications :: Ham Radio",
        ],
        license="GNU General Public License v3 (GPLv3)",
        install_requires=[
            "aprslib>=0.7.2",
            "apprise>=1.9.4",
            "expiringdict>=1.2.2",
            "unidecode>=1.4.0",
            "apscheduler>=3.11.0",
        ],
        keywords=["Ham Radio", "Amateur Radio", "APRS"],
    )
