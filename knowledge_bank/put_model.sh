#!/bin/bash

while getopts t:n:i: flag; do
    case "${flag}" in
    t) MODEL_TYPE=${OPTARG} ;;
    n) MODEL_NAME=${OPTARG} ;;
    i) IP_ADDR=${OPTARG} ;;
    esac
done

echo "Adding '$MODEL_NAME' to '$IP_ADDR'"

# Adding new model to server
curl -X PUT "http://'$IP_ADDR'/admin/model/'$MODEL_NAME'" \
    -F "config=@/master/knowledge_bank/exported_models/'$MODEL_TYPE'/'$MODEL_NAME'/config_aiaa.json;type=application/json" \
    -F "data=@/master/knowledge_bank/exported_models/'$MODEL_TYPE'/'$MODEL_NAME'/model.trt.pb"
