#!/bin/bash

export MODEL_TYPE=prostate
export MODEL_NAME=clara_train_mri_prostate_cg_and_pz_automl_v1

mkdir -p /master/knowledge_bank/exported_models/$MODEL_TYPE/$MODEL_NAME/
chmod a+x export_model.sh
./export_model.sh
