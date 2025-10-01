#!/usr/bin/env/python
#
# Setup file for PyPi publishing work flow via GitHub Actions
# Author: Joerg Schultze-Lutter, 2025
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

from setuptools import setup, find_packages
import os
import re
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit


# Amend this section with your custom data
PACKAGE_SOURCE_DIR = "src"
PACKAGE_NAME = "core-aprs-client"
DESCRIPTION = "Extensible APRS bot framework with dupe detection, beacon/bulletin support and other nice features. Just add your custom APRS bot functions - the APRS bot framework will take care of the rest."
AUTHOR = "Joerg Schultze-Lutter"
AUTHOR_EMAIL = "joerg.schultze.lutter@gmail.com"
URL = "https://github.com/joergschultzelutter/core-aprs-client"
# https://pypi.org/classifiers/
CLASSIFIERS = [
    "Intended Audience :: Developers",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Topic :: Software Development",
    "Operating System :: OS Independent",
    "Development Status :: 4 - Beta",
]
INSTALL_REQUIRES = [
    "aprslib>=0.7.2",
    "apprise>=1.9.4",
    "expiringdict>=1.2.2",
    "unidecode>=1.4.0",
    "apscheduler>=3.11.0",
]
KEYWORDS = ["Ham Radio", "Amateur Radio", "APRS"]
LICENSE = "GNU General Public License v3 (GPLv3)"


# check if the workflow is triggered from within a GitHub action or executed as standalone code
def running_in_a_github_action():
    return os.getenv("GITHUB_ACTIONS") == "true"


# Absolute URL to base repository
BASE_URL = "https://github.com/joergschultzelutter/core-aprs-client/blob/master/"

# Markdown link recognition (will not work on image links)
LINK_RE = re.compile(r"(?<!\!)\[(?P<text>[^\]]+)\]\((?P<href>[^)\s]+)\)")


def is_absolute_url(href: str) -> bool:
    return href.startswith(("http://", "https://", "mailto:"))


def is_root_relative(href: str) -> bool:
    return href.startswith("/")


def looks_like_md(href: str) -> bool:
    path = urlsplit(href).path
    return path.lower().endswith(".md")


def to_absolute_md(href: str) -> str:
    parts = urlsplit(href)  # (scheme, netloc, path, query, fragment)
    abs_url = urljoin(BASE_URL, parts.path)
    return urlunsplit(
        urlsplit(abs_url)._replace(query=parts.query, fragment=parts.fragment)
    )


def rewrite_md_links(md_text: str) -> str:
    def repl(m: re.Match) -> str:
        text = m.group("text")
        href = m.group("href")

        if (
            not is_absolute_url(href)
            and not is_root_relative(href)
            and looks_like_md(href)
        ):
            href = to_absolute_md(href)

        return f"[{text}]({href})"

    return LINK_RE.sub(repl, md_text)


def transform_file(filename: str) -> str:
    in_path = Path(filename)
    if not in_path.exists():
        raise FileNotFoundError(filename)

    content = in_path.read_text(encoding="utf-8")
    transformed = rewrite_md_links(content)
    return transformed


if __name__ == "__main__":
    LONG_DESCRIPTION = transform_file("README.md")

    # PLACEHOLDER for manual package installations via local requirements file
    # git+https://github.com/joergschultzelutter/core-aprs-client#egg=core-aprs-client
    GITHUB_PROGRAM_VERSION = "0.0.1"

    if running_in_a_github_action():
        # Only run this branch if we are part of a GitHub action. Otherwise, just skip
        # it as we won't be able to get the version info from GitHub anyway
        #
        # get VERSION value from GitHub workflow and terminate workflow if value is None
        GITHUB_PROGRAM_VERSION = os.getenv("GITHUB_PROGRAM_VERSION")
        if not GITHUB_PROGRAM_VERSION:
            raise ValueError("Did not receive release label version info from GitHub")
    else:
        if len(GITHUB_PROGRAM_VERSION) == 0:
            raise ValueError(
                "Manual run requires a manually set GITHUB_PROGRAM_VERSION; change setup.py accordingly"
            )

    # Main setup branch
    setup(
        name=PACKAGE_NAME,
        version=GITHUB_PROGRAM_VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        url=URL,
        packages=find_packages(where=PACKAGE_SOURCE_DIR),
        package_dir={"": PACKAGE_SOURCE_DIR},
        include_package_data=True,
        classifiers=CLASSIFIERS,
        license=LICENSE,
        install_requires=INSTALL_REQUIRES,
        keywords=KEYWORDS,
    )
