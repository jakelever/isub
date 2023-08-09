FROM nvidia/cuda:11.3.1-cudnn8-devel-ubuntu20.04

RUN apt update
RUN apt install -y curl wget zip unzip
RUN apt install -y git python3 python3-pip
RUN python3 -m pip install --no-cache-dir --upgrade pip
RUN ln -s /usr/bin/python3 /usr/bin/python

RUN pip install tqdm jsonlines bioc intervaltree
RUN pip install scikit-learn pandas requests

RUN pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu113

RUN pip install transformers tokenizers accelerate datasets sacremoses
RUN pip install ray

# Compile bits-and-bytes
RUN git clone https://github.com/TimDettmers/bitsandbytes.git && cd bitsandbytes && CUDA_VERSION=113 make cuda11x && python setup.py install

RUN pip install networkx scispacy https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.1/en_core_sci_sm-0.5.1.tar.gz matplotlib
