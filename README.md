# Cashier

[![release: v0.1.0](https://img.shields.io/badge/rel-v0.1.0-blue.svg)](https://github.com/arturOnRails/Cashier)
[![main-workflow](https://github.com/arturOnRails/Cashier/actions/workflows/main.yml/badge.svg)](https://github.com/arturOnRails/Cashier/actions)

**Cashier** is a simple library meant for trying out DevOps tools.
It provides a simple, user interactive shopping simulations.
The user is able to buy items for several people.
When finished the software will then produce a bill for each.
This bill lists all bought items and calculates their total price,
while considering their sales taxes.


## Installation

### Install Dependencies

Currently, **Cashier** supports only **Python 3.10** thus it is recommended
to work in a **conda** environment.

```shell
$ conda create -n cashier python=3.10
$ conda activate cashier
```

### Install from GitHub

Latest

```shell
$ pip install git+https://github.com/arturOnRails/Cashier.git
```

Specific release

```shell
$ pip install git+https://github.com/arturOnRails/Cashier.git@<TAG>#egg=Cashier
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

### Development

Building docs requires a linux distribution
and the following dependencies:

- make
- pandoc
