# Gym Xiangqi
Gym Xiangqi is a reinforcement learning environment of Xiangqi, Chinese Chess, game.
The project is built on top of a popular reinforcement learning framework called OpenAI Gym.

## Getting Started
Installing and using Gym Xiangqi easy. If you are unfamiliar with Xiangqi, the Chinese Chess, we encourage 
you to read our [Wiki page](https://github.com/tanliyon/gym-xiangqi/wiki). We also welcome you to checkout our 
[documentation page](https://gym-xiangqi.readthedocs.io/en/latest/), but if you have experience 
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
We are currently working on creating our contribution guidelines.

## Versioning
We use [Semantic Versioning](http://semver.org/) for versioning. For the versions
available, see the [tags on this repository](https://github.com/tanliyon/gym-xiangqi/tags).

## Authors
- Li Yon Tan - [tanliyon](https://github.com/tanliyon)
- Myeonghun Kim - [dooki114](https://github.com/dooki114)
- Hojoung Jang (Brian) - [hojoung97](https://github.com/hojoung97)

## License
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/tanliyon/gym-xiangqi/blob/main/LICENSE) file for details.