#!/bin/bash

export MODEL_TYPE=prostate
export MODEL_NAME=clara_train_mri_prostate_cg_and_pz_automl_v1

# Adding new model to server
curl -X PUT "http://172.17.0.15/admin/model/$MODEL_NAME" \
    -F "config=@exported_models/$MODEL_TYPE/$MODEL_NAME/config_aiaa.json;type=application/json" \
    -F "data=@exported_models/$MODEL_TYPE/$MODEL_NAME/model.trt.pb"
