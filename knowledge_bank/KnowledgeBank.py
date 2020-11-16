import os

from datetime import datetime
from enum import Enum
from typing import List, Union
from py_client import client_api
from tqdm.std import tqdm
from dotenv import load_dotenv

from digital_twin.DicomImages import Image
from digital_twin.DigitalTwin import DigitalTwin
from digital_twin.DigitalTwinPopulation import DigitalTwinPopulation

load_dotenv()

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
        self.last_scan_timestamp: int = 0

    def process_new_images(self):
        updated_digital_twins: List[DigitalTwin] = self.digital_twin_population.get_updated_digital_twins(
            self.last_scan_timestamp)

        digital_twin: DigitalTwin
        for digital_twin in tqdm(updated_digital_twins):
            for image_type in digital_twin.dicom_images.image_types:
                for image_uuid in digital_twin.dicom_images.image_types[image_type]:
                    self.do_aiaa(
                        user_uuid=digital_twin.uuid,
                        image_type=image_type,
                        task_type="segmentation",
                        image_uuid=image_uuid,
                        loaded_user=digital_twin
                    )
                    # TODO: Add inference where possible

        self.last_scan_timestamp = int(datetime.utcnow().timestamp()*1000)

    def do_aiaa(
            self,
            user_uuid: str,
            image_type: str,
            task_type: str,
            image_uuid: str,
            model: str = "",
            loaded_user: Union[DigitalTwin, None] = None) -> None:
        user: Union[DigitalTwin, None] = loaded_user if loaded_user is not None else self.digital_twin_population.get_user_by_id(
            user_uuid)
        if(user is None):
            return

        if(task_type == "segmentation"):
            aiaa_path = self.do_segmentation(
                user, image_type, image_uuid, model
            )
            self.update_aiaa_location(user_uuid, task_type, image_type, image_uuid, aiaa_path)
        elif(task_type == "inference"):
            self.do_inference(
                user, image_type, image_uuid, model
            )

    def do_segmentation(self, user: DigitalTwin, image_type: str, image_uuid: str, model: str = "") -> str:
        image_path, image_name = self.get_image(user, image_type, image_uuid)
        model_to_use = model if model != "" else DefaultSegmentationModels[image_type.upper()].value
        aiaa_path = f'{DATA_SOURCES}\\{image_type}\\segmentations\\{image_name}_seg.nii.gz'
        self.client.segmentation(
            model=model_to_use,
            image_in=image_path,
            image_out=aiaa_path
        )
        return aiaa_path

    def do_inference(self, user: DigitalTwin, image_type: str, image_uuid: str, model: str = ""):
        pass

    def get_image(self, user: DigitalTwin, image_type: str, image_uuid: str):
        image: Image = user.dicom_images.image_types[f'{image_type}'][f'{image_uuid}']
        return image.image_path, image.image_path.split("\\")[-1].split(".nii.gz")[0]

    def update_aiaa_location(
            self,
            user_uuid: str,
            task_type: str,
            image_type: str,
            image_uuid: str,
            path: str
    ):
        attributes = [
            "dicom_images",
            "image_types",
            image_type,
            image_uuid,
            f"{task_type}_path"
        ]
        self.digital_twin_population.update_digital_twin_attribute(user_uuid, attributes, path)
