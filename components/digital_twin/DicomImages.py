from typing import Dict
from datetime import datetime


class Image():
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


class DicomImages():
    def __init__(
        self,
        image_types: Dict[str, Dict[str, Image]] = {},
        lastchanged: int = int(datetime.utcnow().timestamp()*1000)
    ) -> None:
        self.image_types: Dict[str, Dict[str, Image]] = image_types
        self.lastchanged: int = lastchanged

# Example: dicom_images =
# {
#     "lastchanged": 1601658908526,
#     "image_types": {
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
