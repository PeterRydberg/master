#!/bin/bash

while getopts t:n: flag; do
    case "${flag}" in
    t) MODEL_TYPE=${OPTARG} ;;
    n) MODEL_NAME=${OPTARG} ;;
    esac
done

# Do some training
echo "Exporting the frozen model to knowledge bank\n"
./knowledge_generation_engine/clara/export_model.sh -t $MODEL_TYPE -n "$MODEL_NAME\\_$VERSION"
