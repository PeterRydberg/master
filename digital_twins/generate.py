from random import choice, randint
from typing import List, Generic, Dict, TypeVar
from uuid import UUID
from datetime import datetime

import uuid

# Example: {
#   "lungscans":
#       {
#           "created": "2020-09-07 13:47:19.794394",
#           "lastchanged": "2020-09-07 13:47:19.794394",
#           "value": "https://www.somepointer.com/id"
#       }
# }

T = TypeVar('T')


class Appendix(Generic[T]):
    def __init__(self, value: T) -> None:
        self.created: datetime = datetime.now()
        self.lastchanged: datetime = datetime.now()
        self.value: T = value

    def update(self, value: T):
        self.value = value
        self.lastchanged = datetime.now()


class Appendices(Generic[T]):
    def __init__(self) -> None:
        self.appendices: Dict[str, Appendix[T]] = {}
        self.lastchanged: datetime = datetime.now()

    def add(self, key: str, value: T):
        self.appendices[key] = Appendix(value)
        self.lastchanged: datetime = datetime.now()

    def update(self, key: str, value: T):
        self.appendices[key].update(value)
        self.lastchanged = datetime.now()


class User:
    def __init__(self, age: int, sex: str, appendices: Appendices[T] = Appendices()) -> None:
        self.uuid: UUID = uuid.uuid4()
        self.age: int = age
        self.sex: str = sex
        self.appendices: Appendices[T] = appendices


def generate_users(amount: int = 1000) -> List[User]:
    users: List[User] = []

    for _ in range(amount):
        users.append(generate_random_user())

    return users


def generate_random_user() -> User:
    age: int = randint(0, 120)
    sex: str = choice(["male", "female"])

    return User(age, sex)


if __name__ == "__main__":
    users = generate_users()
    users[0].appendices.add("head", "owie")
    users[0].appendices.add("knee", "ouch")
    print(users[0].__dict__)
