FROM nvidia/cuda:12.3.1-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive LANG=C TZ=UTC
ENV TERM=linux


# install some basic utilities
RUN set -xue ;\
    apt-get update -yy ;\
    apt-get upgrade -y ;\
    apt-get install -y --no-install-recommends \
        build-essential \
        libsm6 \
        libxext6 \
        libxrender-dev \
        libglib2.0-0 \
        wget \
        python3-dev \
        python3-pip \
        libgl1 \
        unzip \
        git \
        ffmpeg \
        libavfilter-dev \
        libavformat-dev \
        libavcodec-dev \
        libswresample-dev \
        libavutil-dev \
        tini \
    ;\
    rm -rf /var/lib/apt/lists/*

# Install cuda-toolkit:
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
RUN dpkg -i cuda-keyring_1.1-1_all.deb
RUN apt-get update && apt-get -y install cuda-toolkit-12-5

# update pip
RUN pip3 install --upgrade pip ;\
    pip3 install setuptools

# install pytorch, torchvision and nvidia dali:
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
RUN pip3 install opencv-contrib-python==4.10.0.84
RUN pip3 install ultralytics==8.2.51
RUN pip3 install lapx>=0.5.2

WORKDIR /app/deps/juggling-counting

COPY ./deps/juggling-counting/requirements.txt requirements.txt

# Copy sources:
#COPY ./ /juggling-counting/

# install the requirements:
COPY ./deps/juggling-counting/third_party ./third_party/
RUN pip3 install ./third_party/metrics-gateway-client

# run the command
ENTRYPOINT ["/usr/bin/bash"]

CMD ["run_in_docker.sh"]
