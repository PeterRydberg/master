from typing import List
import uuid
from uuid import UUID


class User:
    def __init__(self, age: int, gender: str):
        self.uuid: UUID = uuid.uuid4()
        self.age: int = age
        self.gender: str = gender


def generate_users(amount: int = 1000):
    users: List[User] = []

    for _ in range(amount):
        users.append(generate_random_user())

    return users


def generate_random_user() -> User:
    return User(1, "male")


if __name__ == "__main__":
    users = generate_users()
    print(users[0].__dict__)
