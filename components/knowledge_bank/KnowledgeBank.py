from __future__ import annotations

import os

from datetime import datetime
from typing import Dict, List, Union
from py_client import client_api
from tqdm.std import tqdm

from SSHClient import SSHClient
from DefaultSegmentationModels import DefaultSegmentationModels
from components.digital_twin.DicomImages import Image
from components.digital_twin.DigitalTwin import DigitalTwin

# In order to use IDE type checking, import is not actually used
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from components.Ecosystem import Ecosystem

from dotenv import load_dotenv
load_dotenv()

DATA_SOURCES = os.getenv('DATA_SOURCE_PATH')
AIAA_SERVER = os.getenv('AIAA_SERVER')


class KnowledgeBank:
    def __init__(self, ecosystem) -> None:
        self.ecosystem: Ecosystem = ecosystem
        self.aiaa_client = client_api.AIAAClient(server_url=AIAA_SERVER)
        self.ssh_client: SSHClient = SSHClient()
        self.last_scan_timestamp: int = 0
        self.models = {}

    def process_new_images(self):
        updated_digital_twins: List[DigitalTwin] = self.ecosystem.digital_twin_population.get_updated_digital_twins(
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
        user: Union[DigitalTwin, None] = loaded_user if loaded_user is not None else (
            self.ecosystem.digital_twin_population.get_user_by_id(user_uuid)
        )
        if(user is None):
            return

        if(task_type == "segmentation"):
            aiaa_path = self.do_segmentation(
                user, image_type, task_type, image_uuid, model
            )
            if(aiaa_path != ""):
                self.update_aiaa_location(user_uuid, task_type, image_type, image_uuid, aiaa_path)
        elif(task_type == "inference"):
            aiaa_path = self.do_inference(
                user, image_type, task_type, image_uuid, model
            )
            if(aiaa_path != ""):
                self.update_aiaa_location(user_uuid, task_type, image_type, image_uuid, aiaa_path)

    def do_segmentation(
        self,
        user: DigitalTwin,
        image_type: str,
        task_type: str,
        image_uuid: str,
        model: str = ""
    ) -> str:
        image_path, image_name = self.get_image(user, image_type, image_uuid)
        model_to_use = self.get_model(image_type, task_type, model)
        if(model_to_use is None):
            return ""
        aiaa_path = f'{DATA_SOURCES}\\{image_type}\\segmentations\\{image_name}_seg.nii.gz'
        self.aiaa_client.segmentation(
            model=model_to_use,
            image_in=image_path,
            image_out=aiaa_path
        )
        return aiaa_path

    def do_inference(
        self,
        user: DigitalTwin,
        image_type: str,
        task_type: str,
        image_uuid: str,
        model: str = "",
        params: Dict[str, str] = {}
    ) -> str:
        image_path, image_name = self.get_image(user, image_type, image_uuid)
        model_to_use = self.get_model(image_type, task_type, model)
        if(model_to_use is None):
            return ""
        aiaa_path = f'{DATA_SOURCES}\\{image_type}\\inferences\\{image_name}_inf.nii.gz'
        self.aiaa_client.inference(
            params=params,
            model=model_to_use,
            image_in=image_path,
            image_out=aiaa_path
        )
        return aiaa_path

    def get_model(self, image_type: str, task_type: str, model: str = ""):
        try:
            use_model = model if model != "" else f'{DefaultSegmentationModels[image_type.upper()].value[task_type]}_v1'
        except KeyError:
            return None

        # Add new model to AIAA server
        # TODO: Make this work by running a batch script instead
        if(use_model == ""):
            pass

        return use_model

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
        self.ecosystem.digital_twin_population.update_digital_twin_attribute(user_uuid, attributes, path)

    def add_model_to_aiaa_server(self, image_type: str, model: str, ip: str):
        command = "./knowledge_bank/put_model.sh"
        flags = f"-t {image_type} -n {model} -i {ip}"
        self.ssh_client.run_ssh_command(command=command, flags=flags, docker=True, container="aiaa_server")
