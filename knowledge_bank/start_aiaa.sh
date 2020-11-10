#!/bin/bash

export MODEL_TYPE=prostate
export MODEL_NAME=clara_train_mri_prostate_cg_and_pz_automl_v1

start_aas.sh --workspace /master/knowledge_bank/exported_models/$MODEL_TYPE/$MODEL_NAME
