from typing import Dict, TypeVar
from datetime import datetime
import uuid


# Types
T = TypeVar('T')


class Appendix(dict):
    def __init__(self, value: T) -> None:
        self.uuid: str = str(uuid.uuid4())
        self.created: datetime = datetime.now()
        self.lastchanged: datetime = datetime.now()
        self.value: T = value

    def update(self, value: T):
        self.value = value
        self.lastchanged = datetime.now()


class Appendices(dict):
    def __init__(self) -> None:
        self.appendices: Dict[str, Dict[str, Appendix]] = {}
        self.lastchanged: datetime = datetime.now()

    def add(self, appendix_type: str, value: T):
        self.appendices[appendix_type] = Appendix(value)
        self.lastchanged = datetime.now()

    def update(self, appendix_type: str, value: T):
        self.appendices[appendix_type].update(value)
        self.lastchanged = datetime.now()

    def delete(self, appendix_type: str):
        del self.appendices[appendix_type]
        self.lastchanged = datetime.now()

# Example: appendices =
# {
#   "lungscans":
#       {
#           "uuid": "some uuid"
#           "created": "2020-09-07 13:47:19.794394",
#           "lastchanged": "2020-09-07 13:47:19.794394",
#           "value": "https://www.somepointer.com/id"
#       }
# }
