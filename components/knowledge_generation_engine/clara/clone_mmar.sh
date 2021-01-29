#!/bin/bash

while getopts t:n: flag; do
    case "${flag}" in
    t) MODEL_TYPE=${OPTARG} ;;
    n) MODEL_NAME=${OPTARG} ;;
    esac
done

printf "\n--- Cloning MMMAR to new model called $MODEL_NAME ---\n"
cp -r /master/components/knowledge_generation_engine/clara/mmar /master/components/knowledge_generation_engine/clara/models/$MODEL_TYPE\/$MODEL_NAME
