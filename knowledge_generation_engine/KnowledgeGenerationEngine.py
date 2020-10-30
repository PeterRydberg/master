from datetime import datetime
from typing import List
from mypy_boto3_dynamodb.service_resource import Table
from tqdm.std import tqdm

from knowledge_bank.KnowledgeBank import KnowledgeBank
from digital_twin.DicomScans import Image

import os
import boto3
import json
import uuid


CONTANING_MODULE = 'knowledge_generation_engine/'


class KnowledgeGenerationEngine:
    def __init__(self,
                 dicom_type,
                 virtual_register="register",
                 knowledge_bank=KnowledgeBank()) -> None:
        self.dicom_type: str = dicom_type
        self.virtual_register: str = virtual_register
        self.virtual_register_path: str = f'{CONTANING_MODULE}{self.virtual_register}.json'
        self.knowledge_bank: KnowledgeBank = knowledge_bank

    def update_virtual_registry(self):
        if(not os.path.isfile(self.virtual_register_path)):
            self.init_register()

        with open(self.virtual_register_path, 'r') as file:
            register = json.load(file)

        next_batch = register['nextBatch']
        last_scan_timestamp = register['lastScanTimestamp']

        new_scans = self.get_new_dicom_scans(last_scan_timestamp)
        register[f'{next_batch}']['dicom_scans'].extend(new_scans)
        register['lastScanTimestamp'] = int(datetime.utcnow().timestamp())
        with open(self.virtual_register_path, 'w') as file:
            json.dump(register, file)

    def get_new_dicom_scans(self, last_scan_timestamp):
        dynamodb = boto3.resource(service_name='dynamodb')
        digital_twin_table: Table = dynamodb.Table('DigitalTwins')
        scan_kwargs = {
            'FilterExpression': 'dicom_scans.lastchanged > :last_scan_timestamp',
            'ExpressionAttributeValues': {
                ':last_scan_timestamp': last_scan_timestamp
            }
        }

        updated_digital_twins = digital_twin_table.scan(**scan_kwargs)
        new_scans: List[Image] = []

        for digital_twin in tqdm(updated_digital_twins['Items']):
            dicom_scans = digital_twin['dicom_scans']
            if(self.dicom_type not in dicom_scans['dicom_categories']):
                continue
            for scan in dicom_scans['dicom_categories'][self.dicom_type]:
                image = dicom_scans['dicom_categories'][self.dicom_type][scan]
                if(int(image['lastchanged']) > last_scan_timestamp and bool(image['share_consent'])):
                    new_scans.append(image['value'])

        return new_scans

    def init_register(self):
        init_batch = str(uuid.uuid4())
        init_file = {
            'nextBatch': init_batch,
            'lastScanTimestamp': 0,
            f'{init_batch}': {
                'trained': False,
                'dicom_scans': []
            }
        }

        with open(self.virtual_register_path, 'x') as file:
            json.dump(init_file, file)

    def set_new_register_batch(self):
        with open(self.virtual_register_path, 'r') as file:
            register = json.load(file)

        next_batch = register['nextBatch']
        register[f'{next_batch}']['trained'] = True

        updated_register = self.create_new_batch(register)
        with open(self.virtual_register_path, 'w') as file:
            json.dump(updated_register, file)

    def create_new_batch(self, register):
        batch_uuid = str(uuid.uuid4())
        register['nextBatch'] = batch_uuid
        register[f'{batch_uuid}'] = {'trained': False, 'dicom_scans': []}

        return register

    def train_virtual_registry_batch(self, batch):
        model = None  # Get latest trained model

        for image in batch:
            # Train model in Clara Train
            pass

        self.export_to_knowledge_base(model=model)  # Export trained model
        self.set_new_register_batch()

    def export_to_knowledge_base(self, model):
        self.knowledge_bank.update_model(self.dicom_type, model)


# Example: registry.json
# DICOM scans points to data sources

# {
#     "nextBatch": "[nextBatchUuid]",
#     "lastScanTimestamp": int,
#     "[batchUuid1]": {
#         "trained": False,
#         "dicom_scans": [
#             "[uuid1]": Image,
#             "[uuid2]": Image,
#             "[uuid3]": Image
#         ]
#     },
#     "[batchUuid2]": {
#         "trained": True,
#         "dicom_scans": [
#             "[uuid4]": Image,
#             "[uuid5]": Image,
#         ]
#     }
# }
