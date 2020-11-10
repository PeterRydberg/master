#!/bin/bash

export MODEL_TYPE=prostate
export MODEL_NAME=clara_train_mri_prostate_cg_and_pz_automl
export VERSION=1

ngc registry model download-version nvidia/med/$MODEL_NAME:$VERSION --dest /master/knowledge_generation_engine/clara/$MODEL_TYPE
chmod a+x export_model.sh
./export_model.sh
