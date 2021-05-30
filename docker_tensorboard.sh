#!/bin/bash

while getopts g: flag; do
    case "${flag}" in
    g) GPUS=${OPTARG} ;;  # e.g. 2
    esac
done


export NVIDIA_RUNTIME="--runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=0"
export OPTIONS="--shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864"
export SOURCE_DIR=/data/hmrydber/master
export MOUNT_DIR=/master
export DOCKER_IMAGE=nvcr.io/nvidia/clara-train-sdk:v3.1.01
export DOCKER_NAME=aiaa_tensorboard
export LOCAL_PORT=9001
export REMOTE_PORT=6006

docker exec -it $DOCKER_NAME /bin/bash \
|| \
docker run $NVIDIA_RUNTIME $OPTIONS -it --rm \
    -p $LOCAL_PORT:$REMOTE_PORT \
    -v $SOURCE_DIR:$MOUNT_DIR \
    -w $MOUNT_DIR \
    --gpus ${GPUS:-0} \
    --name $DOCKER_NAME \
    --user "$(id -u):$(id -g)" -v /etc/passwd:/etc/passwd -v /etc/group:/etc/group \
    $DOCKER_IMAGE \
    /bin/bash
