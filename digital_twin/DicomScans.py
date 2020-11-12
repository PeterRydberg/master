from typing import Dict, TypeVar, Union
from datetime import datetime


T = TypeVar('T')


class Image(dict):
    def __init__(
        self,
        image_path: str,
        segmentation_path=None,
        inference_path=None
    ) -> None:
        self.created: int = int(datetime.utcnow().timestamp()*1000)
        self.lastchanged: int = int(datetime.utcnow().timestamp()*1000)
        self.image_path: str = image_path
        self.segmentation_path: Union[str, None] = segmentation_path
        self.inference_path: Union[str, None] = inference_path
        self.share_consent: bool = False

    def update(self, image_path: str):
        self.lastchanged = int(datetime.utcnow().timestamp()*1000)
        self.image_path = image_path


class DicomScans():
    def __init__(self) -> None:
        self.dicom_categories: Dict[str, Dict[str, Image]] = {}
        self.lastchanged: int = int(datetime.utcnow().timestamp()*1000)

    def add(self, scan_type: str, image_path: str):
        self.dicom_categories[scan_type] = Image(image_path)
        self.lastchanged: int = int(datetime.utcnow().timestamp()*1000)

    def update(self, scan_type: str, image_path: T):
        self.dicom_categories[scan_type].update(image_path)
        self.lastchanged: int = int(datetime.utcnow().timestamp()*1000)

    def delete(self, scan_type: str):
        del self.dicom_categories[scan_type]
        self.lastchanged: int = int(datetime.utcnow().timestamp()*1000)


# Example: dicom_scans =
# {
#     "lastchanged": 1601658908526,
#     "dicom_categories": {
#         "heart": {
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
