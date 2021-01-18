#!/bin/bash

while getopts t:n:i: flag; do
    case "${flag}" in
    t) MODEL_TYPE=${OPTARG} ;;
    n) MODEL_NAME=${OPTARG} ;;
    i) IP_ADDR=${OPTARG} ;;
    esac
done

printf "\n--- Adding model $MODEL_NAME to AIAA server on $IP_ADDR ---\n"
curl -X PUT "http://$IP_ADDR/admin/model/$MODEL_NAME" \
    -F "config=@/master/components/knowledge_bank/exported_models/$MODEL_TYPE/$MODEL_NAME/config_aiaa.json;type=application/json" \
    -F "data=@/master/components/knowledge_bank/exported_models/$MODEL_TYPE/$MODEL_NAME/model.trt.pb"
