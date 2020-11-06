from typing import Dict, TypeVar
from datetime import datetime


T = TypeVar('T')


class Image(dict):
    def __init__(self, value: T) -> None:
        self.created: int = int(datetime.utcnow().timestamp()*1000)
        self.lastchanged: int = int(datetime.utcnow().timestamp()*1000)
        self.value: T = value
        self.share_consent: bool = False

    def update(self, value: T):
        self.lastchanged = int(datetime.utcnow().timestamp()*1000)
        self.value = value


class DicomScans(dict):
    def __init__(self) -> None:
        self.dicom_categories: Dict[str, Dict[str, Image]] = {}
        self.lastchanged: int = int(datetime.utcnow().timestamp()*1000)

    def add(self, scan_type: str, value: T):
        self.dicom_categories[scan_type] = Image(value)
        self.lastchanged: int = int(datetime.utcnow().timestamp()*1000)

    def update(self, scan_type: str, value: T):
        self.dicom_categories[scan_type].update(value)
        self.lastchanged: int = int(datetime.utcnow().timestamp()*1000)

    def delete(self, scan_type: str):
        del self.dicom_categories[scan_type]
        self.lastchanged: int = int(datetime.utcnow().timestamp()*1000)


# Example: dicom_scans =
# {
#     "lastchanged": 1601658908526,
#     "dicom_categories": {
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
