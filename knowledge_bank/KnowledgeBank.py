import os

from enum import Enum
from typing import Union
from py_client import client_api

from digital_twin.DicomScans import Image
from digital_twin.DigitalTwin import DigitalTwin
from digital_twin.DigitalTwinPopulation import DigitalTwinPopulation


DATA_SOURCES = os.getenv('DATA_SOURCE_PATH')


class DefaultSegmentationModels(Enum):
    BRAINTUMOUR = ""
    HEART = ""
    HIPPOCAMPUS = ""
    PROSTATE = "clara_train_mri_prostate_cg_and_pz_automl_v1"


class KnowledgeBank:
    def __init__(self, digital_twin_population=DigitalTwinPopulation()) -> None:
        self.models = {}
        self.client = client_api.AIAAClient(server_url='http://129.241.113.190:9000/')
        self.digital_twin_population: DigitalTwinPopulation = digital_twin_population

    def do_aiaa(self, user_id: str, task_type: str, organ: str, image_uuid: str, model: str = ""):
        user: Union[DigitalTwin, None] = self.digital_twin_population.get_user_by_id(user_id)
        if(user is None):
            return

        if(task_type == "segmentation"):
            self.do_segmentation(
                user, organ, image_uuid, model
            )
        elif(task_type == "inference"):
            self.do_inference(
                user, organ, image_uuid, model
            )

    def do_segmentation(self, user: DigitalTwin, organ: str, image_uuid: str, model: str = ""):
        image_path, image_name = self.get_image(user, organ, image_uuid)
        model_to_use = model if model != "" else DefaultSegmentationModels[organ.upper()].value
        self.client.segmentation(
            model=model_to_use,
            image_in=image_path,
            image_out=f'{DATA_SOURCES}\\{organ}\\segmentations\\{image_name}_seg.nii.gz'
        )
        return

    def do_inference(self, user: DigitalTwin, organ: str, image_uuid: str, model: str = ""):
        pass

    def get_image(self, user: DigitalTwin, organ: str, image_uuid: str):
        image: Image = user.dicom_scans.dicom_categories[f'{organ}'][f'{image_uuid}']
        return image.image_path, image.image_path.split('nii.gz')[0]
