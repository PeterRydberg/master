#!/bin/bash

while getopts t:n:v: flag; do
    case "${flag}" in
    t) MODEL_TYPE=${OPTARG} ;;
    n) MODEL_NAME=${OPTARG} ;;
    v) VERSION=${OPTARG} ;;
    esac
done

ngc registry model download-version nvidia/med/$MODEL_NAME:$VERSION --dest /master/knowledge_generation_engine/clara/$MODEL_TYPE
chmod a+x export_model.sh
./export_model.sh -t $MODEL_TYPE -n "'$MODEL_NAME'_'$VERSION'"
