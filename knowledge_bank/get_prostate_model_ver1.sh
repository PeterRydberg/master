#!/bin/bash

MODEL_NAME=clara_train_mri_prostate_cg_and_pz_automl
VERSION=1

ngc registry model download-version nvidia/med/$MODEL_NAME:$VERSION --dest /knowledge_bank/exported_models/prostate
