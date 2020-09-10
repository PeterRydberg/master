from random import choice, randint, random, sample
from typing import List
from usertypes import Appendices
from uuid import UUID

import uuid

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
        self.uuid: UUID = uuid.uuid4()
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


if __name__ == "__main__":
    users = generate_users()
    users[0].appendices.add("head", "owie")
    users[0].appendices.add("knee", "ouch")
    users[0].appendices.delete("knee")
    print(users[0].__dict__)
