#!/bin/bash

while getopts t:n:v: flag; do
    case "${flag}" in
    t) MODEL_TYPE=${OPTARG} ;;
    n) MODEL_NAME=${OPTARG} ;;
    v) VERSION=${OPTARG} ;;
    esac
done

printf "\n--- Getting new model $MODEL_NAME and setting it to the knowledge generation engine ---\n"
mkdir -p /master/components/knowledge_generation_engine/clara/$MODEL_TYPE
ngc registry model download-version nvidia/med/$MODEL_NAME:$VERSION --dest /master/components/knowledge_generation_engine/clara/$MODEL_TYPE
chmod 700 -R /master/components/knowledge_generation_engine/clara/$MODEL_TYPE

./components/knowledge_generation_engine/clara/export_model.sh -t $MODEL_TYPE -n $MODEL_NAME\_v$VERSION
