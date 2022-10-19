FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y build-essential cmake libboost-dev libzmq3-dev python3 python3-zmq git

RUN mkdir /simulation

ADD https://framagit.org/simgrid/simgrid/-/archive/v3.31/simgrid-v3.31.tar.gz /simulation
WORKDIR /simulation
RUN tar -xvzf simgrid-v3.31.tar.gz
WORKDIR /simulation/simgrid-v3.31
RUN cmake -DCMAKE_INSTALL_PREFIX=/simulation/simgrid .
RUN make -j12
RUN make install

RUN git clone https://github.com/elastisim/elastisim.git /simulation/elastisim
WORKDIR /simulation/elastisim
RUN cmake -DCMAKE_INSTALL_PREFIX=/simulation/elastisim -DSIMGRID_SOURCE_DIR=/simulation/simgrid -DCMAKE_BUILD_TYPE="Release" .
RUN make -j12

WORKDIR /simulation/
RUN git clone https://github.com/elastisim/elastisim-python.git
ENV PYTHONPATH "${PYTHONPATH}:/simulation/elastisim-python"

WORKDIR /
ENTRYPOINT ["/simulation/elastisim/elastisim"]