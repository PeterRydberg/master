from enum import Enum


# Fetched pretrained models are appended _v{VERSION} to their MMAR directory name
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
        "segmentation": "clara_train_mri_prostate_cg_and_pz_automl"
    }
    C19_LUNG_LESION = {
        "segmentation": "clara_train_covid19_ct_lesion_seg"
    }
    C19_LUNG_SEG = {
        "segmentation": "clara_train_covid19_ct_lung_seg"
    }
