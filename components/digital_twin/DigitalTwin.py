from typing import List, Union
from .DicomImages import DicomImages

import uuid as uuid_getter


class DigitalTwin:
    def __init__(self,
                 age: int,
                 sex: str,
                 firstname: str,
                 lastname: str,
                 uuid: Union[str, None] = None,
                 conditions: List[str] = [],
                 dicom_images: DicomImages = DicomImages(),
                 models: List = []
                 ) -> None:
        self.uuid: str = uuid if uuid is not None else str(uuid_getter.uuid4())
        self.age: int = age
        self.sex: str = sex
        self.firstname: str = firstname
        self.lastname: str = lastname
        self.conditions: List[str] = conditions
        self.dicom_images: DicomImages = dicom_images
        self.models = models

    def update_twin_info(self):
        pass
