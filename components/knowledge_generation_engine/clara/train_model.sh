#!/bin/bash

while getopts t:n:f: flag; do
    case "${flag}" in
    t) MODEL_TYPE=${OPTARG} ;;
    n) MODEL_NAME=${OPTARG} ;;
    f) BASH_FILE=${OPTARG} ;;
    esac
done

printf "\n--- Training on model $MODEL_NAME using traing command $BASH_FILE ---\n"
./components/knowledge_generation_engine/clara/$MODEL_TYPE\/$MODEL_NAME\/commands\/$BASH_FILE

printf "\n--- Exporting models to frozen versions ---\n"
./components/knowledge_generation_engine/clara/$MODEL_TYPE\/$MODEL_NAME\/commands/export.sh
./components/knowledge_generation_engine/clara/export_model.sh -t $MODEL_TYPE -n "$MODEL_NAME\\_$VERSION"
