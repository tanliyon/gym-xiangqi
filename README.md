# Gym Xiangqi

![CI Test Suite](https://github.com/tanliyon/gym-xiangqi/actions/workflows/main.yml/badge.svg)
![flake8 lint](https://github.com/tanliyon/gym-xiangqi/actions/workflows/lint.yml/badge.svg)
![radon analysis](https://github.com/tanliyon/gym-xiangqi/actions/workflows/radon.yml/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/gym-xiangqi/badge/?version=latest)](https://gym-xiangqi.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/gym-xiangqi.svg)](https://badge.fury.io/py/gym-xiangqi)

Gym Xiangqi is a reinforcement learning environment of Xiangqi, Chinese Chess, game.
The project is built on top of a popular reinforcement learning framework called OpenAI Gym.

![Welcome Demo](resources/welcome_demo.gif)

## Getting Started
Installing and using Gym Xiangqi is easy. If you are unfamiliar with Xiangqi, the Chinese Chess, we encourage 
you to read our [Wiki page](https://github.com/tanliyon/gym-xiangqi/wiki) for a starter. We also welcome you to 
checkout our [documentation page](https://gym-xiangqi.readthedocs.io/en/latest/), but if you have experiences 
working with other OpenAI Gym environments you will be already off to a good start.

### Prerequisites
In order to use Gym Xiangqi environment for your reinforcement learning project,
you need to have,
- A machine that supports video and audio outputs. For example, a headless server
will not be a great choice here.
- Python 3.6 or above

### User Installation
Install Gym Xiangqi on your Python environment using `pip`
```
pip install gym-xiangqi
```
Test your installation by running
```
agent-v-agent
```

### Development Installation
First, clone the repository
```
git clone https://github.com/tanliyon/gym-xiangqi.git
```
or download the [latest release](https://github.com/tanliyon/gym-xiangqi/releases)
and extract the files


Enter the repository
```
cd gym-xiangqi
```

Install the core dependencies
```
pip install -e .
```

Install the dependencies for development
```
pip install -r requirements.txt
```

## Software Handbook
Read through the [software handbook](https://docs.google.com/document/d/1Y5AM-Xj4XUkurKW1m9cBOs0bRJWS62qw8wu74Alcj9k/edit?usp=sharing) for comprehensive explanation and development guide for the repository.

## Built With
- [OpenAI Gym] - Used for developing the reinforcement learning environment
- [PyGame] - Used for rendering the game 

## Contributing
Please checkout our contribution guidelines in [CONTRIBUTING.md](CONTRIBUTING.md) and our 
[software handbook](https://docs.google.com/document/d/1Y5AM-Xj4XUkurKW1m9cBOs0bRJWS62qw8wu74Alcj9k/edit?usp=sharing).

## Versioning
We use [Semantic Versioning](http://semver.org/) for versioning. For the versions
available, see the [tags on this repository](https://github.com/tanliyon/gym-xiangqi/tags).

## Authors
- Li Yon Tan - [tanliyon](https://github.com/tanliyon)
- Myeonghun Kim (Danny) - [dooki114](https://github.com/dooki114)
- Hojoung Jang (Brian) - [hojoung97](https://github.com/hojoung97)

## License
This project is licensed under the GNU Lesser General Public License v3.0 - see the [LICENSE.md](https://github.com/tanliyon/gym-xiangqi/blob/main/LICENSE) file for details.