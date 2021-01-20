#!/usr/bin/env bash

my_dir="$(dirname "$0")"
. $my_dir/set_env.sh

echo "MMAR_ROOT set to $MMAR_ROOT"

additional_options="$*"

# Data list containing all data
python -u -m nvmidl.apps.automl.train \
    -m $MMAR_ROOT \
    --set \
    run_id=test1 \
    workers=0:1 \
    ${additional_options}
