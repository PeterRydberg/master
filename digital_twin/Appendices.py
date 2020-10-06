from typing import Dict, TypeVar
from datetime import datetime


T = TypeVar('T')


class Image(dict):
    def __init__(self, value: T) -> None:
        self.created: datetime = datetime.now()
        self.lastchanged: datetime = datetime.now()
        self.value: T = value

    def update(self, value: T):
        self.value = value
        self.lastchanged = datetime.now()


class Appendices(dict):
    def __init__(self) -> None:
        self.appendices: Dict[str, Dict[str, Image]] = {}
        self.lastchanged: datetime = datetime.now()

    def add(self, appendix_type: str, value: T):
        self.appendices[appendix_type] = Image(value)
        self.lastchanged = datetime.now()

    def update(self, appendix_type: str, value: T):
        self.appendices[appendix_type].update(value)
        self.lastchanged = datetime.now()

    def delete(self, appendix_type: str):
        del self.appendices[appendix_type]
        self.lastchanged = datetime.now()


# Example: appendices =
# {
#     "lastchanged": 1601658908526,
#     "appendices": {
#         "lungscans": {
#             "[uuid]"{
#                 "created": 1601658908526,
#                 "lastchanged": 1601658908526,
#                 "value": "[data_source]"
#             }
#             "[uuid2]"{
#                 "created": 1601658908526,
#                 "lastchanged": 1601658908526,
#                 "value": "[data_source]"
#             }
#         }
#     }
# }
