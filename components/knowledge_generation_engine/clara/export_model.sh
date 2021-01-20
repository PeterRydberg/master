#!/bin/bash

while getopts t:n: flag; do
    case "${flag}" in
    t) MODEL_TYPE=${OPTARG} ;;
    n) MODEL_NAME=${OPTARG} ;;
    esac
done

printf "\n--- Exporting model $MODEL_NAME to knowledge bank ---\n"
mkdir -p /master/components/knowledge_bank/exported_models/$MODEL_TYPE/$MODEL_NAME/
chmod 755 /master/components/knowledge_bank/exported_models/$MODEL_TYPE/$MODEL_NAME/
chmod 644 /master/components/knowledge_generation_engine/clara/models/$MODEL_TYPE/$MODEL_NAME/{models/model.fzn.pb,models/model.trt.pb,config/config_aiaa.json}
cp /master/components/knowledge_generation_engine/clara/models/$MODEL_TYPE/$MODEL_NAME/{models/model.fzn.pb,models/model.trt.pb,config/config_aiaa.json} /master/components/knowledge_bank/exported_models/$MODEL_TYPE/$MODEL_NAME/
