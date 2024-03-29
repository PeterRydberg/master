from __future__ import annotations

import os
import shutil
import json
import uuid

from collections import defaultdict
from datetime import datetime
from typing import Dict, List
from tqdm.std import tqdm

from SSHClient import SSHClient
from DefaultSegmentationModels import DefaultSegmentationModels
from components.digital_twin.DigitalTwin import DigitalTwin
from components.digital_twin.DicomImages import Image
from .data_preparation import prepare_LUNA16_training_data_remote, prepare_MID_training_data_remote, prepare_batch_training_data_remote

# In order to use IDE type checking, import is not actually used
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from components.Ecosystem import Ecosystem


KGE_PATH = '/master/components/knowledge_generation_engine/'
VIRTUAL_REGISTERS = 'components\\knowledge_generation_engine\\virtual_registers'
EXTERNAL_REGISTERS = 'components\\knowledge_generation_engine\\external_registers'
DICOM_TYPES = ['braintumour', 'heart', 'hippocampus', 'prostate']


class KnowledgeGenerationEngine:
    def __init__(self, ecosystem) -> None:
        self.ecosystem: Ecosystem = ecosystem
        self.ssh_client: SSHClient = SSHClient()

    def update_virtual_register(self, image_type: str):
        virtual_register_dir_path = f'{VIRTUAL_REGISTERS}\\{image_type}'
        virtual_register_path = f'{virtual_register_dir_path}\\register.json'

        if(not os.path.isfile(virtual_register_path)):
            self.init_register(virtual_register_dir_path, virtual_register_path)

        with open(virtual_register_path, 'r') as file:
            register = json.load(file)

        next_batch_uuid = register['nextBatch']
        last_scan_timestamp = register['lastScanTimestamp']
        self.add_updated_images_to_register(
            image_type=image_type,
            batch=register[f'{next_batch_uuid}']['dicom_images'],
            last_scan_timestamp=last_scan_timestamp
        )
        register['lastScanTimestamp'] = int(datetime.utcnow().timestamp()*1000)

        with open(virtual_register_path, 'w') as file:
            json.dump(register, file, indent=4)

    def add_updated_images_to_register(self, image_type: str, batch: Dict[str, Dict], last_scan_timestamp: int):
        updated_digital_twins: List[DigitalTwin] = self.ecosystem.digital_twin_population.get_updated_digital_twins(
            last_scan_timestamp)

        digital_twin: DigitalTwin
        for digital_twin in tqdm(updated_digital_twins):
            dicom_images = digital_twin.dicom_images
            if(image_type not in dicom_images.image_types):
                continue
            for image_uuid in dicom_images.image_types[image_type]:
                image = dicom_images.image_types[image_type][image_uuid]
                file_name = image.image_path.split("\\")[-1].split(".nii.gz")[0]
                if(
                    int(image.lastchanged) > last_scan_timestamp
                    and bool(image.aiaa_consented)
                    and bool(image.aiaa_approved)

                ):
                    register = self.update_batch_image(image_type, image_uuid, file_name, image)
                    batch.update(register)
                elif(
                    int(image.lastchanged) > last_scan_timestamp
                    and (not bool(image.aiaa_consented)
                         or not bool(image.aiaa_approved))
                ):
                    self.delete_file(image_type, "image", file_name)
                    self.delete_file(image_type, "segmentation", file_name)
                    self.delete_file(image_type, "inference", file_name)
                    batch.pop(image_uuid, None)

        return batch

    # Copies images directly from Data Sources into the Virtual Register
    def update_batch_image(self, image_type: str, image_uuid: str, file_name: str, image: Image):
        register = defaultdict(defaultdict)

        if(image.image_path != ''):
            image_path = shutil.copy(
                image.image_path,
                self.get_file_path(image_type, "image", file_name)
            )
            register[f'{image_uuid}']['image_path'] = image_path

        if(image.segmentation_path != ''):
            segmentation_path = shutil.copy(
                image.segmentation_path,
                self.get_file_path(image_type, "segmentation", file_name)
            )
            register[f'{image_uuid}']['segmentation_path'] = segmentation_path
        else:
            self.delete_file(image_type, "segmentation", file_name)

        if(image.inference_path != ''):
            inference_path = shutil.copy(
                image.inference_path,
                self.get_file_path(image_type, "inference", file_name)
            )
            register[f'{image_uuid}']['inference_path'] = inference_path
        else:
            self.delete_file(image_type, "inference", file_name)

        return register

    def get_file_path(self, image_type: str, task_type: str, file_name: str):
        file_path = ""
        if(task_type == "image"):
            file_name = f'{file_name}.nii.gz'
            file_path = f'.\\{VIRTUAL_REGISTERS}\\{image_type}\\images\\{file_name}'
        elif(task_type == "segmentation"):
            file_name_seg = f'{file_name}_seg.nii.gz'
            file_path = f'.\\{VIRTUAL_REGISTERS}\\{image_type}\\segmentations\\{file_name_seg}'
        elif(task_type == "inference"):
            file_name_inf = f'{file_name}_inf.nii.gz'
            file_path = f'.\\{VIRTUAL_REGISTERS}\\{image_type}\\inferences\\{file_name_inf}'

        return file_path

    def delete_file(self, image_type, task_type, file_name):
        file_path = self.get_file_path(image_type, task_type, file_name)
        if(os.path.isfile(file_path)):
            os.remove(file_path)

    def init_register(self, virtual_register_dir_path: str, virtual_register_path: str):
        init_batch = str(uuid.uuid4())
        init_file = {
            'nextBatch': init_batch,
            'lastScanTimestamp': 0,
            f'{init_batch}': {
                'trained': False,
                'dicom_images': {}
            }
        }

        os.makedirs(os.path.dirname(f'{virtual_register_dir_path}\\images\\'), exist_ok=True)
        os.makedirs(os.path.dirname(f'{virtual_register_dir_path}\\segmentations\\'), exist_ok=True)
        os.makedirs(os.path.dirname(f'{virtual_register_dir_path}\\inferences\\'), exist_ok=True)

        with open(virtual_register_path, 'x') as file:
            json.dump(init_file, file, indent=4)

    def set_new_register_batch(self, virtual_register_path: str):
        with open(virtual_register_path, 'r') as file:
            register = json.load(file)

        next_batch = register['nextBatch']
        register[f'{next_batch}']['trained'] = True

        updated_register = self.create_new_batch(register)
        with open(virtual_register_path, 'w') as file:
            json.dump(updated_register, file, indent=4)

    def create_new_batch(self, register):
        batch_uuid = str(uuid.uuid4())
        register['nextBatch'] = batch_uuid
        register[f'{batch_uuid}'] = {'trained': False, 'dicom_images': []}

        return register

    def add_pretrained_model(self, image_type: str, model: str, version: str):
        command = "./components/knowledge_generation_engine/clara/get_pretrained_model.sh"
        flags = f"-t {image_type} -n {model} -v {version}"
        self.ssh_client.run_ssh_command(command=command, flags=flags, docker=True, container="aiaa_training")

    def train_external_dataset(
            self,
            image_type: str,
            task_type: str,
            model: str = "",
            use_existing_mmar: bool = False,
            finetune: bool = False,
            gpu: str = "",  # "_2gpu OR _4gpu"
            validation_split: float = 0.3,
            dataset_name: str = "",
            dataset_subsets: list[str] = [""],
    ):
        train_file = f"train{gpu.lower()}_finetune.sh" if finetune else f"train{gpu.lower()}.sh"

        # Configures remote training to use already downloaded dataset
        # prepare_MID_training_data_remote(
        #     image_type,
        #     task_type,
        #     model,
        #     use_existing_mmar,
        #     validation_split,
        #     dataset_name,
        #     self.ssh_client
        # )

        prepare_LUNA16_training_data_remote(
            image_type,
            task_type,
            model,
            use_existing_mmar,
            validation_split,
            dataset_subsets,
            self.ssh_client
        )
        return

        # Start training command
        command = "./components/knowledge_generation_engine/clara/train_model.sh"
        flags = f"-t {image_type} -n {model} -f {train_file}"
        self.ssh_client.run_ssh_command(command=command, flags=flags, docker=True, container="aiaa_training")

    def train_virtual_register_batch(
        self,
        image_type: str,
        task_type: str,
        model: str = None,
        batch_id: str = None,
        finetune: bool = False,
        finetune_path: str = "",
        gpu: str = "",  # "_2gpu OR _4gpu"
        update_batch: bool = True,
        validation_split: float = 0.3
    ):
        virtual_register_path = f'{VIRTUAL_REGISTERS}\\{image_type}\\register.json'
        with open(virtual_register_path, 'r') as file:
            register = json.load(file)

        model_str = f'{DefaultSegmentationModels[image_type.upper()].value[task_type]}_v1' if model is None else model
        batch_no = register["nextBatch"] if batch_id is None else batch_id
        train_file = f"train{gpu.lower()}_finetune.sh" if finetune else f"train{gpu.lower()}.sh"

        # Physically moves registry batch to remote server for training
        prepare_batch_training_data_remote(
            image_type,
            task_type,
            model_str,
            register[batch_no]["dicom_images"],
            finetune_path,
            validation_split,
        )

        # Start training command
        command = "./components/knowledge_generation_engine/clara/train_model.sh"
        flags = f"-t {image_type} -n {model_str} -f {train_file}"
        self.ssh_client.run_ssh_command(command=command, flags=flags, docker=True, container="aiaa_training")

        if(update_batch):
            self.set_new_register_batch(virtual_register_path=virtual_register_path)

# Example: register.json
# DICOM images point to data sources

# {
#     'nextBatch': '[nextBatchUuid]',
#     'lastScanTimestamp': int,
#     '[batchUuid1]': {
#         'trained': False,
#         'dicom_images': [
#             '[uuid1]': Image,
#             '[uuid2]': Image,
#             '[uuid3]': Image
#         ]
#     },
#     '[batchUuid2]': {
#         'trained': True,
#         'dicom_images': [
#             '[uuid4]': Image,
#             '[uuid5]': Image,
#         ]
#     }
# }
