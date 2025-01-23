#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import platform
import re
import sys
import textwrap

import setuptools


if sys.version_info < (3, ):
    raise ImportError(textwrap.dedent("""\
        You are trying to install medieval_chess on Python 2.

        The last compatible branch was 0.23.x, which was supported until the
        end of 2018. Consider upgrading to Python 3.
        """))

if sys.version_info < (3, 8):
    raise ImportError(textwrap.dedent("""\
        You are trying to install medieval_chess.

        Since version 1.11.0, medieval_chess requires Python 3.8 or later.
        Since version 1.0.0, medieval_chess requires Python 3.7 or later.
        """))

import medieval_chess as medieval_chess


def read_description():
    """
    Reads the description from README.rst and substitutes mentions of the
    latest version with a concrete version number.
    """
    with open(os.path.join(os.path.dirname(__file__), "README.rst"), encoding="utf-8") as f:
        description = f.read()

    # Link to the documentation of the specific version.
    description = description.replace(
        "//medieval-medieval_chess.readthedocs.io/en/latest/",
        "//medieval-medieval_chess.readthedocs.io/en/v{}/".format(medieval_chess.__version__))

    # Use documentation badge for the specific version.
    description = description.replace(
        "//readthedocs.org/projects/medieval-medieval_chess/badge/?version=latest",
        "//readthedocs.org/projects/medieval-medieval_chess/badge/?version=v{}".format(medieval_chess.__version__))

    # Remove doctest comments.
    description = re.sub(r"\s*# doctest:.*", "", description)

    return description


setuptools.setup(
    name="medieval-chess",
    version=medieval_chess.__version__,
    author=medieval_chess.__author__,
    author_email=medieval_chess.__email__,
    description=medieval_chess.__doc__.replace("\n", " ").strip(),
    long_description=read_description(),
    long_description_content_type="text/x-rst",
    license="GPL-3.0+",
    keywords="medieval_chess fen epd pgn polyglot syzygy gaviota uci xboard",
    url="https://github.com/alvaro-francisco-gil/medieval-medieval_chess",
    packages=["medieval_chess"],
    test_suite="test",
    zip_safe=False,  # For mypy
    package_data={
        "medieval_chess": ["py.typed"],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Games/Entertainment :: Board Games",
        "Topic :: Games/Entertainment :: Turn Based Strategy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Typing :: Typed",
    ],
    project_urls={
        "Documentation": "https://medieval-medieval_chess.readthedocs.io",
    }
)
