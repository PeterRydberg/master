#!/bin/bash

export MODEL_TYPE=prostate
export MODEL_NAME=clara_train_mri_prostate_cg_and_pz_automl

train.sh
export.sh

cp /master/knowledge_generation_engine/clara/$MODEL_TYPE/$MODEL_NAME/model.fzn.pb /master/knowledge_bank/exported_models/$MODEL_TYPE/$MODEL_NAME/
cp /master/knowledge_generation_engine/clara/$MODEL_TYPE/$MODEL_NAME/model.trt.pb /master/knowledge_bank/exported_models/$MODEL_TYPE/$MODEL_NAME/
