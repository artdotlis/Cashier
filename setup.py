# -*- coding: utf-8 -*-
"""
Packaging Python Projects.

See Also
--------
    `https://packaging.python.org/tutorials/packaging-projects/`_
"""
from pathlib import Path
import setuptools  # type: ignore

from src.cashier.version import VERSION


with Path("README.md").open("r", encoding="utf-8") as fh_read_me:
    READ_ME = fh_read_me.read()

setuptools.setup(
    name="Cashier",
    version=VERSION,
    author="Artur Lissin",
    author_email="arturOnRails@protonmail.com",
    maintainer="Artur Lissin",
    maintainer_email="arturOnRails@protonmail.com",
    description="Library for calculating sales taxes.",
    long_description=READ_ME,
    long_description_content_type="text/markdown",
    url="https://github.com/arturOnRails/Cashier",
    platforms=["Linux"],
    license='MIT License',
    packages=setuptools.find_packages(),
    python_requires="==3.10",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License"
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'cashier=src.main:main'
        ]
    }
)
