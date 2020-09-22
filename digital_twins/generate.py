from random import choice, randint, random, sample
from tqdm import tqdm

from typing import List
from mypy_boto3_dynamodb.service_resource import Table
from botocore.exceptions import ClientError
from typings.usertypes import Appendices

import uuid
import boto3
import names

# From https://www.medicalschemes.com/medical_schemes_pmb/chronic_disease_list.htm
chronic_diseases: List[str] = [
    "Addison's disease", "Asthma", "Bronchiectasis", "Cardiac failure", "Cardiomyopathy",
    "Chronic obstructive pulmonary disorder", "Chronic renal disease", "Coronary artery disease", "Crohn's disease",
    "Diabetes insipidus", "Diabetes mellitus types 1 & 2", "Dysrhythmias", "Epilepsy", "Glaucoma", "Haemophilia",
    "Hyperlipidaemia", "Hypertension", "Hypothyroidism", "Multiple sclerosis", "Parkinson's disease",
    "Rheumatoid arthritis", "Schizophrenia", "Systemic lupus erythematosus", "Ulcerative colitis",
    "Bipolar Mood Disorder"]


class User:
    def __init__(self,
                 age: int,
                 sex: str,
                 firstname: str,
                 lastname: str,
                 conditions: List[str] = [],
                 appendices: Appendices = Appendices()
                 ) -> None:
        self.uuid: str = str(uuid.uuid4())
        self.age: int = age
        self.sex: str = sex
        self.firstname: str = firstname
        self.lastname: str = lastname
        self.conditions: List[str] = conditions
        self.appendices: Appendices = appendices


def generate_users(amount: int = 1000) -> List[User]:
    users: List[User] = []

    for _ in range(amount):
        users.append(generate_random_user())

    return users


def generate_random_user() -> User:
    age: int = randint(0, 120)
    sex: str = choice(["male", "female"])
    firstname: str = names.get_first_name(gender=sex)
    lastname: str = names.get_last_name()
    conditions: List[str] = sample(chronic_diseases, 1 if random() > 0.97 else 0)

    return User(age, sex, firstname, lastname, conditions)


def update_dynamodb(users: List[User]) -> None:
    dynamodb = boto3.resource(service_name='dynamodb')
    user_table: Table = dynamodb.Table('Users')

    try:
        user_table.creation_date_time
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == "ResourceNotFoundException":
            print("Creating new table...")
            user_table = create_users_table(table_name="Users")
            print("Table created!")
        else:
            print(e)

    for user in tqdm(users):
        dict_user = vars(user)
        user_table.put_item(Item=dict_user)

    print(f"\n{len(users)} users added to DynamoDB.")


def create_users_table(table_name: str, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'uuid',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'lastname',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'uuid',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'lastname',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table


if __name__ == "__main__":
    users = generate_users(amount=100)
    update_dynamodb(users)
