#!/bin/bash

export NVIDIA_RUNTIME="--runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=0"
export OPTIONS="--shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864"
export SOURCE_DIR=/home/hmrydber/Prosjekter/master
export MOUNT_DIR=/master
export LOCAL_PORT=9000
export REMOTE_PORT=80
export DOCKER_NAME=hmrydber/aiaa_server
export DOCKER_IMAGE=nvcr.io/nvidia/clara-train-sdk:v3.1

docker run $NVIDIA_RUNTIME $OPTIONS -it --rm \
-p $LOCAL_PORT:$REMOTE_PORT \
-v $SOURCE_DIR:$MOUNT_DIR \
-w $MOUNT_DIR \
--name $DOCKER_NAME \
$DOCKER_IMAGE \
/bin/bash
