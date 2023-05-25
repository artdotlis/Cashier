# Cashier

[![release: v0.2.0](https://img.shields.io/badge/rel-v0.2.0-blue.svg)](https://github.com/artdotlis/Cashier)
[![GitHub](https://img.shields.io/github/license/artdotlis/Cashier)](https://raw.githubusercontent.com/artdotlis/Cashier/main/LICENSE)
[![main](https://github.com/artdotlis/Cashier/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/artdotlis/Cashier/actions/workflows/main.yml)
[![Documentation Status](https://img.shields.io/badge/docs-GitHub-blue.svg?style=flat-square)](https://artdotlis.github.io/Cashier/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


**Cashier** is a simple library meant for trying out DevOps tools.
It provides a simple, user interactive shopping simulations.
The user is able to buy items for several people.
When finished the software will then produce a bill for each.
This bill lists all bought items and calculates their total price,
while considering their sales taxes.


## Installation

### Install Dependencies

Currently, **Cashier** supports only **Python 3.11** thus it is recommended
to work in a **conda** environment.

```shell
$ conda create -n cashier python=3.11
$ conda activate cashier
```

### Install from GitHub

Latest

```shell
$ pip install git+https://github.com/artdotlis/Cashier.git
```

Specific release

```shell
$ pip install git+https://github.com/artdotlis/Cashier.git@<TAG>#egg=Cashier
```

## Usage

For more information use:

```shell
$ cashier -h
```

Quickstart with default values:

```shell
$ cashier
```

## Development

Requires a linux distribution and the following dependencies:

### Default

-   pyenv: ~2.13
-   GNU/Linux

### Dev Container

-   Docker
-   Docker - Compose
