#!/bin/bash

while getopts t:n: flag; do
    case "${flag}" in
    t) MODEL_TYPE=${OPTARG} ;;
    n) MODEL_NAME=${OPTARG} ;;
    esac
done

python3 -m tensorboard.main --logdir models/$MODEL_TYPE/$MODEL_NAME/
