export MODEL_TYPE=prostate
export MODEL_NAME=clara_train_mri_prostate_cg_and_pz_automl_v1

mkdir -p /master/knowledge_bank/exported_models/$MODEL_TYPE/$MODEL_NAME/
cp /master/knowledge_generation_engine/clara/$MODEL_TYPE/$MODEL_NAME/{models/model.fzn.pb,models/model.trt.pb,config/config_aiaa.json} /master/knowledge_bank/exported_models/$MODEL_TYPE/$MODEL_NAME/
