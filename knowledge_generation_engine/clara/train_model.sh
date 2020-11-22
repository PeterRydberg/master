#!/bin/bash

while getopts t:n: flag; do
    case "${flag}" in
    t) MODEL_TYPE=${OPTARG} ;;
    n) MODEL_NAME=${OPTARG} ;;
    esac
done

# Do some training
echo "Exporting the frozen model to knowledge bank\n"
chmod a+x export_model.sh
./export_model.sh
