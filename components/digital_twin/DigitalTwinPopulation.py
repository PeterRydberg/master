from __future__ import annotations

import os
import boto3

from botocore.exceptions import ClientError
from mypy_boto3_dynamodb.service_resource import Table
from typing import Dict, List, Union

from components.digital_twin.DicomImages import DicomImages, Image
from .DigitalTwin import DigitalTwin
from .generate import create_and_set_digital_twins

# In order to use IDE type checking, import is not actually used
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from components.Ecosystem import Ecosystem

from dotenv import load_dotenv
load_dotenv()


class DigitalTwinPopulation:
    def __init__(self, ecosystem) -> None:
        self.ecosystem: Ecosystem = ecosystem
        self.digital_twins_cache: Union[List[DigitalTwin], None] = []
        self.dynamodb = boto3.resource(
            service_name='dynamodb',
            region_name="eu-west-2",
            aws_access_key_id=os.getenv('AWS_PUBLIC_KEY'),
            aws_secret_access_key=os.getenv('AWS_SECRET_KEY')
        )

    def get_updated_digital_twins(self, last_scan_timestamp: int) -> List[DigitalTwin]:
        digital_twin_table: Table = self.dynamodb.Table('DigitalTwins')
        scan_kwargs = {
            'FilterExpression': 'dicom_images.lastchanged > :last_scan_timestamp',
            'ExpressionAttributeValues': {
                ':last_scan_timestamp': last_scan_timestamp
            }
        }

        try:
            response = digital_twin_table.scan(**scan_kwargs)
        except ClientError as e:
            print(e.response['Error']['Message'])
            return []
        else:
            digital_twin: List[DigitalTwin] = [self.pythonize_digital_twin(x) for x in response["Items"]]
            return digital_twin

    def generate_new_population(self, size: int) -> None:
        self.digital_twins_cache = create_and_set_digital_twins(
            dynamodb=self.dynamodb,
            size=size
        )

    def get_user_by_id(self, user_uuid: str) -> Union[DigitalTwin, None]:
        return next(
            (user for user in self.digital_twins_cache if user.uuid == user_uuid),
            self.get_user_by_id_aws(user_uuid)
        )

    def get_user_by_id_aws(self, user_uuid: str) -> Union[DigitalTwin, None]:
        digital_twin_table: Table = self.dynamodb.Table('DigitalTwins')

        try:
            response = digital_twin_table.get_item(Key={'uuid': user_uuid})
        except ClientError as e:
            print(e.response['Error']['Message'])
            return None
        else:
            digital_twin: DigitalTwin = self.pythonize_digital_twin(response["Item"])
            self.digital_twins_cache.append(digital_twin)
            return digital_twin

    def pythonize_digital_twin(self, dt_dict) -> DigitalTwin:
        digital_twin: DigitalTwin = DigitalTwin(**dt_dict)
        dicom_images: DicomImages = DicomImages(**digital_twin.dicom_images)
        digital_twin.dicom_images = dicom_images
        for image_type in dicom_images.image_types:
            for image_uuid in dicom_images.image_types[image_type]:
                image: Image = Image(**dicom_images.image_types[image_type][image_uuid])
                dicom_images.image_types[image_type][image_uuid] = image

        return digital_twin

    def update_digital_twin_attribute(
        self,
        uuid: str,
        attributes: List[str],
        value: Union[str, bool, int, float]
    ):
        table = self.dynamodb.Table('DigitalTwins')

        attribute_dict, attribute_string = self.spread_attributes(attributes)
        params = {
            'Key': {'uuid': uuid},
            'ReturnValues': 'ALL_NEW',
            'UpdateExpression': f'set {attribute_string} = :val',
            'ExpressionAttributeNames': attribute_dict,
            'ExpressionAttributeValues': {
                ':val': value
            }
        }
        table.update_item(**params)

    def spread_attributes(self, attributes):
        attribute_dict: Dict[str, str] = {}
        attribute_string: str = ""

        for index, attribute in enumerate(attributes):
            attr_letter = chr(ord('`')+index+1)
            attribute_dict[f'#{attr_letter}'] = attribute
            attribute_string += f'#{attr_letter}.'

        return attribute_dict, attribute_string[:-1]
