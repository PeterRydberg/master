#!/bin/bash

while getopts t:n: flag; do
    case "${flag}" in
    t) MODEL_TYPE=${OPTARG} ;;
    n) MODEL_NAME=${OPTARG} ;;
    esac
done

mkdir -p /master/knowledge_bank/exported_models/$MODEL_TYPE/$MODEL_NAME/
chmod a+x export_model.sh
./export_model.sh
