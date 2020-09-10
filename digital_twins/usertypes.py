from typing import Generic, Dict, TypeVar
from datetime import datetime


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
