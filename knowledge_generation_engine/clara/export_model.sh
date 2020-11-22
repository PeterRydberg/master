#!/bin/bash

while getopts t:n: flag; do
    case "${flag}" in
    t) MODEL_TYPE=${OPTARG} ;;
    n) MODEL_NAME=${OPTARG} ;;
    esac
done

mkdir -p /master/knowledge_bank/exported_models/$MODEL_TYPE/$MODEL_NAME/
chmod 755 /master/knowledge_bank/exported_models/$MODEL_TYPE/$MODEL_NAME/
chmod 644 /master/knowledge_generation_engine/clara/$MODEL_TYPE/$MODEL_NAME/{models/model.fzn.pb,models/model.trt.pb,config/config_aiaa.json}
cp /master/knowledge_generation_engine/clara/$MODEL_TYPE/$MODEL_NAME/{models/model.fzn.pb,models/model.trt.pb,config/config_aiaa.json} /master/knowledge_bank/exported_models/$MODEL_TYPE/$MODEL_NAME/
