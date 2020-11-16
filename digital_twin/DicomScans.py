from typing import Dict, TypeVar, Union
from datetime import datetime


T = TypeVar('T')


class Image(dict):
    def __init__(
        self,
        created: int = int(datetime.utcnow().timestamp()*1000),
        lastchanged: int = int(datetime.utcnow().timestamp()*1000),
        image_path: str = "",
        segmentation_path="",
        inference_path="",
        aiaa_consented: bool = False,
        aiaa_approved: bool = False
    ) -> None:
        self.created: int = created
        self.lastchanged: int = lastchanged
        self.image_path: str = image_path
        self.segmentation_path: str = segmentation_path
        self.inference_path: str = inference_path
        self.aiaa_consented: bool = aiaa_consented
        self.aiaa_approved: bool = aiaa_approved

    def update(self, image_path: str):
        self.lastchanged = int(datetime.utcnow().timestamp()*1000)
        self.image_path = image_path


class DicomScans():
    def __init__(
        self,
        dicom_categories: Dict[str, Dict[str, Image]] = {},
        lastchanged: int = int(datetime.utcnow().timestamp()*1000)
    ) -> None:
        self.dicom_categories: Dict[str, Dict[str, Image]] = dicom_categories
        self.lastchanged: int = lastchanged

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
#                 [paths, aiaa consent, etc]
#             }
#             "[uuid2]"{
#                 "created": 1601658908526,
#                 "lastchanged": 1601658908526,
#                 [paths, aiaa consent, etc]
#             }
#         }
#     }
# }
