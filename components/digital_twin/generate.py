import json
import boto3
import names
from random import choice, randint, random, sample
from tqdm import tqdm
from typing import List
from mypy_boto3_dynamodb.service_resource import Table
from botocore.exceptions import ClientError

from .DigitalTwin import DigitalTwin


# From https://www.medicalschemes.com/medical_schemes_pmb/chronic_disease_list.htm
chronic_diseases: List[str] = [
    "Addison's disease", "Asthma", "Bronchiectasis", "Cardiac failure", "Cardiomyopathy",
    "Chronic obstructive pulmonary disorder", "Chronic renal disease", "Coronary artery disease", "Crohn's disease",
    "Diabetes insipidus", "Diabetes mellitus types 1 & 2", "Dysrhythmias", "Epilepsy", "Glaucoma", "Haemophilia",
    "Hyperlipidaemia", "Hypertension", "Hypothyroidism", "Multiple sclerosis", "Parkinson's disease",
    "Rheumatoid arthritis", "Schizophrenia", "Systemic lupus erythematosus", "Ulcerative colitis",
    "Bipolar Mood Disorder"]


def generate_digital_twins(amount: int = 1000) -> List[DigitalTwin]:
    digital_twins: List[DigitalTwin] = []

    for _ in range(amount):
        digital_twins.append(generate_random_digital_twin())

    return digital_twins


def generate_random_digital_twin() -> DigitalTwin:
    age: int = randint(0, 120)
    sex: str = choice(["male", "female"])
    firstname: str = names.get_first_name(gender=sex)
    lastname: str = names.get_last_name()
    conditions: List[str] = sample(chronic_diseases, 1 if random() > 0.97 else 0)

    return DigitalTwin(
        age=age,
        sex=sex,
        firstname=firstname,
        lastname=lastname,
        conditions=conditions
    )


def update_dynamodb(dynamodb, digital_twins: List[DigitalTwin]) -> None:
    digital_twin_table: Table = dynamodb.Table('DigitalTwins')

    try:
        digital_twin_table.creation_date_time
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == "ResourceNotFoundException":
            print("Creating new table...")
            digital_twin_table = create_digital_twins_table(dynamodb, table_name="DigitalTwins")
            print("Table created!")
        else:
            print(e)

    for digital_twin in tqdm(digital_twins):
        dict_digital_twin = obj_to_json(digital_twin)
        digital_twin_table.put_item(Item=dict_digital_twin)

    print(f"\n{len(digital_twins)} digital twins added to DynamoDB.")


def create_digital_twins_table(dynamodb, table_name: str):
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'uuid',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'uuid',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table


def obj_to_json(obj):
    return json.loads(
        json.dumps(obj, default=lambda o: getattr(o, '__dict__', str(o)))
    )


def create_and_set_digital_twins(dynamodb, size: int = 100):
    try:
        digital_twins = generate_digital_twins(amount=size)
        update_dynamodb(dynamodb, digital_twins)
        return digital_twins
    except Exception as e:
        print("Error creating new digital twin population:", e)


if __name__ == "__main__":
    dynamodb = boto3.resource(service_name='dynamodb')
    create_and_set_digital_twins(dynamodb)
