class User:
    def __init__(self, age: int):
        self.age: int = age


if __name__ == "__main__":
    user: User = User(age=15)
    print(user.age)
