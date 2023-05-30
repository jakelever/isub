FROM nvidia/cuda:11.3.1-cudnn8-devel-ubuntu20.04
#FROM pytorch/pytorch:1.12.1-cuda11.3-cudnn8-runtime

RUN apt update
RUN apt install -y git python3 python3-pip
RUN python3 -m pip install --no-cache-dir --upgrade pip

RUN python3 -m pip install tqdm jsonlines bioc intervaltree
RUN python3 -m pip install scikit-learn pandas

RUN python3 -m pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu113

RUN python3 -m pip install transformers tokenizers accelerate datasets bitsandbytes sacremoses
RUN python3 -m pip install ray
