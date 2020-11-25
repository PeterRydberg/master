from enum import Enum


class DefaultSegmentationModels(Enum):
    BRAINTUMOUR = {
        "segmentation": "clara_mri_seg_brain_tumors_br16_full_amp"
    }
    HEART = {
        "segmentation": ""
    }
    HIPPOCAMPUS = {
        "segmentation": ""
    }
    SPLEEN = {
        "segmentation": "clara_ct_seg_spleen_amp"
    }
    PROSTATE = {
        "segmentation": "clara_train_mri_prostate_cg_and_pz_automl_v1"
    }
