#!/usr/bin/env python3
"""Setup the Traiter environment."""

import re
from setuptools import setup, find_packages


def readme():
    """Get README.md content."""
    with open("README.md", 'r') as f:
        return f.read()


def license_():
    """Get LICENSE.txt content."""
    with open("LICENSE", 'r') as f:
        return f.read()


def find_version():
    """Read version from db.py."""
    regex = r"^__VERSION__ = ['\"]v?([^'\"]*)['\"]"
    with open("./traiter/util.py", 'r') as f:
        match = re.search(regex, f.read(), re.M)
        if match:
            return match.group(1)

    raise RuntimeError("Unable to find version string.")


def find_requirements():
    """Read requirements.txt file and returns list of requirements."""
    with open("requirements.txt", 'r') as f:
        return f.read().splitlines()


setup(
    name="traiter",
    version=find_version(),
    packages=find_packages(),
    install_requires=find_requirements(),
    description="""Traiter""",
    long_description=readme(),
    license=license_(),
    url="https://github.com/rafelafrance/traiter",
    python_requires='>=3.8',
    scripts=[])
