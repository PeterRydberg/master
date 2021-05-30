#!/bin/bash

while getopts g: flag; do
    case "${flag}" in
    g) GPUS=${OPTARG} ;;  # e.g. 2
    esac
done


export NVIDIA_RUNTIME="--runtime=nvidia" #-e NVIDIA_VISIBLE_DEVICES=0"
export OPTIONS="--shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864"
export SOURCE_DIR=/source
export MOUNT_DIR=/mount
export DOCKER_IMAGE=nvcr.io/nvidia/clara-train-sdk:v3.1.01
export DOCKER_NAME=aiaa_federated_learning
export LOCAL_PORT=9002
export REMOTE_PORT=8002
export LOCAL_PORT_ADM=9003
export REMOTE_PORT_ADM=8003

docker exec -it $DOCKER_NAME /bin/bash \
|| \
docker run $NVIDIA_RUNTIME $OPTIONS -it --rm \
    -p $LOCAL_PORT:$REMOTE_PORT \
    -p $LOCAL_PORT_ADM:$REMOTE_PORT_ADM \
    -v $SOURCE_DIR:$MOUNT_DIR \
    -w $MOUNT_DIR \
    --gpus ${GPUS:-0} \
    --name $DOCKER_NAME \
    $DOCKER_IMAGE \
    /bin/bash
