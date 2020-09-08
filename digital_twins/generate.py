from random import choice, randint, random, sample
from typing import List, Generic, Dict, TypeVar
from uuid import UUID
from datetime import datetime

import uuid

# From https://www.medicalschemes.com/medical_schemes_pmb/chronic_disease_list.htm
chronic_diseases: List[str] = [
    "Addison's disease", "Asthma", "Bronchiectasis", "Cardiac failure", "Cardiomyopathy",
    "Chronic obstructive pulmonary disorder", "Chronic renal disease  ", "Coronary artery disease", "Crohn's disease  ",
    "Diabetes insipidus", "Diabetes mellitus types 1 & 2", "Dysrhythmias  ", "Epilepsy", "Glaucoma  ", "Haemophilia",
    "Hyperlipidaemia", "Hypertension", "Hypothyroidism", "Multiple sclerosis", "Parkinson's disease",
    "Rheumatoid arthritis", "Schizophrenia", "Systemic lupus erythematosus", "Ulcerative colitis",
    "Bipolar Mood Disorder"]


# Types
T = TypeVar('T')


class Appendix(Generic[T]):
    def __init__(self, value: T) -> None:
        self.created: datetime = datetime.now()
        self.lastchanged: datetime = datetime.now()
        self.value: T = value

    def update(self, value: T):
        self.value = value
        self.lastchanged = datetime.now()


class Appendices():
    def __init__(self) -> None:
        self.appendices: Dict[str, Appendix[T]] = {}
        self.lastchanged: datetime = datetime.now()

    def add(self, key: str, value: T):
        self.appendices[key] = Appendix(value)
        self.lastchanged: datetime = datetime.now()

    def update(self, key: str, value: T):
        self.appendices[key].update(value)
        self.lastchanged = datetime.now()

    def delete(self, key: str):
        del self.appendices[key]
        self.lastchanged = datetime.now()

# Example: {
#   "lungscans":
#       {
#           "created": "2020-09-07 13:47:19.794394",
#           "lastchanged": "2020-09-07 13:47:19.794394",
#           "value": "https://www.somepointer.com/id"
#       }
# }


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
    print(users[0])
    print("Amount of users with chronic diseases is", sum(1 for user in users if user.conditions != []))
