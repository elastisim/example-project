FROM debian:bookworm-slim AS builder

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y build-essential cmake pkg-config libboost-dev \
    libzmq3-dev python3 python3-venv python3-pip git wget && \
    rm -rf /var/lib/apt/lists/*

RUN wget -qP /build https://framagit.org/simgrid/simgrid/-/archive/v3.34/simgrid-v3.34.tar.gz && \
    tar -xzf /build/simgrid-v3.34.tar.gz -C /build && \
    cd /build/simgrid-v3.34 && \
    cmake -DCMAKE_INSTALL_PREFIX=/usr/local -DCMAKE_BUILD_TYPE="Release" . && \
    make -j$(nproc) && \
    make install

RUN git clone https://github.com/elastisim/elastisim.git /build/elastisim && \
    cd /build/elastisim && \
    cmake -DCMAKE_INSTALL_PREFIX=/usr/local -DCMAKE_BUILD_TYPE="Release" . && \
    make -j$(nproc) && \
    make install

FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends libzmq5 git && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local /usr/local
RUN ldconfig

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN git clone https://github.com/elastisim/elastisim-python.git /build/elastisim-python && \
    pip install --upgrade pip && \
    pip install /build/elastisim-python

RUN rm -rf /build

ENTRYPOINT ["/usr/local/bin/elastisim"]
