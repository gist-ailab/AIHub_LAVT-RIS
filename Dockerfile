# Base image with CUDA and Ubuntu 20.04 (development version)
FROM nvidia/cuda:11.1.1-cudnn8-devel-ubuntu20.04

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    bzip2 \
    git \
    build-essential \
    python3-dev \
    libgl1-mesa-dev \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Miniconda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda && \
    rm Miniconda3-latest-Linux-x86_64.sh

# Update PATH environment variable
ENV PATH=/opt/conda/bin:$PATH

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements_aws.txt .

# Create Conda environment and install packages
RUN conda create -n lavt python=3.7 -y && \
    /bin/bash -c "source /opt/conda/bin/activate lavt && \
    pip install cython && \
    pip install torch==1.8.1+cu111 torchvision==0.9.1+cu111 torchaudio==0.8.1 -f https://download.pytorch.org/whl/torch_stable.html && \
    pip install -r requirements_aws.txt"

# Update PATH for the environment
ENV PATH=/opt/conda/envs/lavt/bin:$PATH
RUN conda init bash

# Copy application code
COPY . .

# Set default shell to bash
SHELL ["/bin/bash", "-c"]
