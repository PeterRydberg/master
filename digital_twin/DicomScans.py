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


class DicomScans(dict):
    def __init__(self) -> None:
        self.dicom_scans: Dict[str, Dict[str, Image]] = {}
        self.lastchanged: datetime = datetime.now()

    def add(self, scan_type: str, value: T):
        self.dicom_scans[scan_type] = Image(value)
        self.lastchanged = datetime.now()

    def update(self, scan_type: str, value: T):
        self.dicom_scans[scan_type].update(value)
        self.lastchanged = datetime.now()

    def delete(self, scan_type: str):
        del self.dicom_scans[scan_type]
        self.lastchanged = datetime.now()


# Example: dicom_scans =
# {
#     "lastchanged": 1601658908526,
#     "dicom_scans": {
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
