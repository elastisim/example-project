# ElastiSim Example Project

An example ElastiSim project utilizing an FCFS algorithm (without backfill) applied on 32 rigid jobs with alternating compute and I/O phases running on a crossbar topology with 128 compute nodes.

## Installation

To build the containers that are required to run ElastiSim, install Docker and execute the following commands:
```sh
docker build -t elastisim -f Dockerfile.elastisim .
docker build -t elastisim-python -f Dockerfile.elastisim-python .
```

## Simulation

To run the simulation, execute the following commands in two different sessions:

### \*nix:
```sh
docker run -v $PWD/data:/data -u `id -u $USER` -v /tmp --name elastisim -it --rm elastisim /data/input/configuration.json --log=root.thresh:warning
docker run -v $PWD/algorithm:/algorithm -u `id -u $USER` --volumes-from elastisim -it --rm elastisim-python
```

### Mac OS:
```sh
docker run -v $PWD/data:/data -v /tmp --name elastisim -it --rm elastisim /data/input/configuration.json --log=root.thresh:warning
docker run -v $PWD/algorithm:/algorithm --volumes-from elastisim -it --rm elastisim-python
```

### Windows (PowerShell):
```sh
docker run -v ${PWD}\data:/data -v /tmp --name elastisim -it --rm elastisim /data/input/configuration.json --log=root.thresh:warning
docker run -v ${PWD}\algorithm:/algorithm --volumes-from elastisim -it --rm elastisim-python
```

The first container runs ElastiSim and accepts two inputs:
- the configuration file (JSON)
- the logging level

For a more detailed output change `--log=root.thresh:warning` to `--log=root.thresh:info` (caution: verbose)

The second container runs the scheduling algorithm. Both containers communicate via inter-process communication using the first container's temporary directory.
