from collections import defaultdict
from datetime import datetime
from mypy_boto3_dynamodb.service_resource import Table
from tqdm.std import tqdm

from knowledge_bank.KnowledgeBank import KnowledgeBank

import os
import shutil
import boto3
import json
import uuid


VIRTUAL_REGISTRIES = 'knowledge_generation_engine\\virtual_registries'
DICOM_TYPES = ['braintumour', 'heart', 'hippocampus', 'prostate']


class KnowledgeGenerationEngine:
    def __init__(self,
                 dicom_type,
                 knowledge_bank=KnowledgeBank()) -> None:
        self.dicom_type: str = dicom_type
        self.virtual_register_path: str = f'{VIRTUAL_REGISTRIES}\\{self.dicom_type}'
        self.virtual_register: str = f'{self.virtual_register_path}\\registry.json'
        self.knowledge_bank: KnowledgeBank = knowledge_bank

    def update_virtual_registry(self):
        if(not os.path.isfile(self.virtual_register)):
            self.init_register()

        with open(self.virtual_register, 'r') as file:
            register = json.load(file)

        next_batch_uuid = register['nextBatch']
        last_scan_timestamp = register['lastScanTimestamp']
        self.get_new_dicom_scans(register[f'{next_batch_uuid}']['dicom_scans'], last_scan_timestamp)

        register['lastScanTimestamp'] = int(datetime.utcnow().timestamp()*1000)
        with open(self.virtual_register, 'w') as file:
            json.dump(register, file, indent=4)

    def get_new_dicom_scans(self, batch, last_scan_timestamp):
        dynamodb = boto3.resource(service_name='dynamodb')
        digital_twin_table: Table = dynamodb.Table('DigitalTwins')
        scan_kwargs = {
            'FilterExpression': 'dicom_scans.lastchanged > :last_scan_timestamp',
            'ExpressionAttributeValues': {
                ':last_scan_timestamp': last_scan_timestamp
            }
        }

        updated_digital_twins = digital_twin_table.scan(**scan_kwargs)

        for digital_twin in tqdm(updated_digital_twins['Items']):
            dicom_scans = digital_twin['dicom_scans']
            if(self.dicom_type not in dicom_scans['dicom_categories']):
                continue
            for scan in dicom_scans['dicom_categories'][self.dicom_type]:
                image = dicom_scans['dicom_categories'][self.dicom_type][scan]
                file_name = image["image_path"].split("\\")[-1].split(".nii.gz")[0]
                if(
                    int(image['lastchanged']) > last_scan_timestamp
                    and bool(image['aiaa_consented'])
                    and bool(image['aiaa_approved'])

                ):
                    registry = self.update_batch_image(image, scan, file_name)
                    batch.update(registry)
                elif(
                    int(image['lastchanged']) > last_scan_timestamp
                    and (not bool(image['aiaa_consented'])
                         or not bool(image['aiaa_approved']))
                ):
                    self.delete_file("image", file_name)
                    self.delete_file("segmentation", file_name)
                    self.delete_file("inference", file_name)
                    batch.pop(scan, None)

        return batch

    # Copies images directly from Data Sources into the Virtual Registry
    def update_batch_image(self, image, scan, file_name):
        registry = defaultdict(defaultdict)

        if(image['image_path'] != ''):
            image_path = shutil.copy(
                image['image_path'],
                self.get_file_path("image", file_name)
            )
            registry[f'{scan}']['image_path'] = image_path

        if(image['segmentation_path'] != ''):
            segmentation_path = shutil.copy(
                image['segmentation_path'],
                self.get_file_path("segmentation", file_name)
            )
            registry[f'{scan}']['segmentation_path'] = segmentation_path
        else:
            self.delete_file("segmentation", file_name)

        if(image['inference_path'] != ''):
            inference_path = shutil.copy(
                image['inference_path'],
                self.get_file_path("inference", file_name)
            )
            registry[f'{scan}']['inference_path'] = inference_path
        else:
            self.delete_file("inference", file_name)

        return registry

    def get_file_path(self, type, file_name):
        file_path = ""
        if(type == "image"):
            file_name = f'{file_name}.nii.gz'
            file_path = f'.\\{VIRTUAL_REGISTRIES}\\{self.dicom_type}\\images\\{file_name}'
        elif(type == "segmentation"):
            file_name_seg = f'{file_name}_seg.nii.gz'
            file_path = f'.\\{VIRTUAL_REGISTRIES}\\{self.dicom_type}\\segmentations\\{file_name_seg}'
        elif(type == "inference"):
            file_name_inf = f'{file_name}_inf.nii.gz'
            file_path = f'.\\{VIRTUAL_REGISTRIES}\\{self.dicom_type}\\inferences\\{file_name_inf}'

        return file_path

    def delete_file(self, type, file_name):
        file_path = self.get_file_path(type, file_name)
        if(os.path.isfile(file_path)):
            os.remove(file_path)

    def init_register(self):
        init_batch = str(uuid.uuid4())
        init_file = {
            'nextBatch': init_batch,
            'lastScanTimestamp': 0,
            f'{init_batch}': {
                'trained': False,
                'dicom_scans': {}
            }
        }

        os.makedirs(os.path.dirname(f'{self.virtual_register_path}\\images\\'), exist_ok=True)
        os.makedirs(os.path.dirname(f'{self.virtual_register_path}\\segmentations\\'), exist_ok=True)
        os.makedirs(os.path.dirname(f'{self.virtual_register_path}\\inferences\\'), exist_ok=True)

        with open(self.virtual_register, 'x') as file:
            json.dump(init_file, file, indent=4)

    def set_new_register_batch(self):
        with open(self.virtual_register, 'r') as file:
            register = json.load(file)

        next_batch = register['nextBatch']
        register[f'{next_batch}']['trained'] = True

        updated_register = self.create_new_batch(register)
        with open(self.virtual_register, 'w') as file:
            json.dump(updated_register, file, indent=4)

    def create_new_batch(self, register):
        batch_uuid = str(uuid.uuid4())
        register['nextBatch'] = batch_uuid
        register[f'{batch_uuid}'] = {'trained': False, 'dicom_scans': []}

        return register

    def train_virtual_registry_batch(self, batch):
        # TODO: Make this work by running a batch script instead
        # (train.sh and train_finetune.sh)
        model = None  # Get latest trained model

        for image in batch:
            # Train model in Clara Train
            pass

        self.export_to_knowledge_base(model=model)  # Export trained model
        self.set_new_register_batch()

    def export_to_knowledge_base(self, model):
        # TODO: Make this work by running a batch script instead
        # (export.sh)
        # self.knowledge_bank.update_model(self.dicom_type, model)
        pass


# Example: registry.json
# DICOM scans points to data sources

# {
#     'nextBatch': '[nextBatchUuid]',
#     'lastScanTimestamp': int,
#     '[batchUuid1]': {
#         'trained': False,
#         'dicom_scans': [
#             '[uuid1]': Image,
#             '[uuid2]': Image,
#             '[uuid3]': Image
#         ]
#     },
#     '[batchUuid2]': {
#         'trained': True,
#         'dicom_scans': [
#             '[uuid4]': Image,
#             '[uuid5]': Image,
#         ]
#     }
# }
