# tugger-routing: Case-Study on Reinforcement Learning for Assembly Line Material Supply

This repository shows the application of reinforcement learning to solve a particular production logistics problem dealing with the coordination of material supply for an assembly process.

## Quick-Start

Train an ppo-agent (by default for only 10,000 steps, which should take <1min):

```sh
docker-compose up ppo-training
```

Tilemap-animation of the trained agent (not yet awesome after only 10k steps) (visit <http://localhost:5000>):

```sh
docker-compose up ppo-web-animation-tilemap
```

(see commands in docker-compose.yml for info on which scripts are executable)
