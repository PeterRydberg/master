from random import choice, randint, random, sample
from typing import List
from typings.usertypes import Appendices
from tqdm import tqdm

import uuid
import boto3

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
                 conditions: List[str] = [],
                 appendices: Appendices = Appendices()
                 ) -> None:
        self.uuid: str = str(uuid.uuid4())
        self.age: int = age
        self.sex: str = sex
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
    conditions: List[str] = sample(chronic_diseases, 1 if random() > 0.97 else 0)

    return User(age, sex, conditions)


def update_dynamodb(users: List[User]) -> None:
    dynamodb = boto3.resource('dynamodb')
    user_table = dynamodb.Table('User')

    for user in tqdm(users):
        dict_user = vars(user)
        user_table.put_item(Item=dict_user)

    print(f"\n{len(users)} users added to DynamoDB.")


if __name__ == "__main__":
    users = generate_users(amount=1000)
    update_dynamodb(users)
