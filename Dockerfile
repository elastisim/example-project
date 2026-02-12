FROM debian:bookworm-slim AS builder

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y build-essential cmake pkg-config libboost-dev libzmq3-dev python3 python3-venv python3-pip git wget
RUN rm -rf /var/lib/apt/lists/*

RUN mkdir /build

WORKDIR /build
RUN wget https://framagit.org/simgrid/simgrid/-/archive/v3.34/simgrid-v3.34.tar.gz 
RUN tar -xvzf simgrid-v3.34.tar.gz
WORKDIR /build/simgrid-v3.34
RUN cmake -DCMAKE_INSTALL_PREFIX=/usr/local .
RUN make -j$(nproc)
RUN make install

WORKDIR /build
RUN git clone https://github.com/elastisim/elastisim.git
WORKDIR /build/elastisim
RUN cmake -DCMAKE_INSTALL_PREFIX=/usr/local -DCMAKE_BUILD_TYPE="Release" .
RUN make -j$(nproc)
RUN make install

FROM python:3.12-slim

RUN apt-get update
RUN apt-get install -y --no-install-recommends libzmq5 git
RUN rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local /usr/local
RUN ldconfig

RUN git clone https://github.com/elastisim/elastisim-python.git /build/elastisim-python
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install /build/elastisim-python

WORKDIR /
RUN rm -rf /build

ENTRYPOINT ["/usr/local/bin/elastisim"]
