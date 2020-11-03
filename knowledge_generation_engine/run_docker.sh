#!/bin/bash
export dockerImage=nvcr.io/nvidia/clara-train-sdk:v3.0
docker run -it --rm --gpus all --shm-size=1G --ulimit memlock=-1 --ulimit stack=67108864 -v /home/hmrydber/Prosjekter/master:/workspace/master $dockerImage /bin/bash
