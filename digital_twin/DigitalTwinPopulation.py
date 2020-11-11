import boto3
from collections import namedtuple
from botocore.exceptions import ClientError
from mypy_boto3_dynamodb.service_resource import Table
from typing import Dict, List, Union

from .DigitalTwin import DigitalTwin
from .generate import create_and_set_digital_twins


class DigitalTwinPopulation:
    def __init__(self) -> None:
        self.digital_twins_cache: Union[List[DigitalTwin], None] = []
        self.dynamodb = boto3.resource(service_name='dynamodb')

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
        else:
            digital_twin: DigitalTwin = DigitalTwin(**response["Item"])
            self.digital_twins_cache.append(digital_twin)
            return digital_twin

    def customDigitalTwinDecoder(self, digital_twin_dict: Dict):
        return namedtuple('X', digital_twin_dict.keys())(*digital_twin_dict.values())
