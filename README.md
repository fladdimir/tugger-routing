# tugger-routing: Case-Study on Reinforcement Learning for Assembly Line Material Supply

This repository shows the application of reinforcement learning to solve a particular production logistics problem dealing with the coordination of material supply for an assembly process.

## Quick-Start

Train an ACER-agent (by default for only 10,000 steps, which should take <1min):

```sh
docker-compose up acer-training
```

Plot performance (might require additional steps for connecting the display):

```sh
docker-compose up acer-plot-training
```

Tilemap-animation of the trained agent (visit <http://localhost:5000>):

```sh
docker-compose up acer-web-animation-tilemap
```
