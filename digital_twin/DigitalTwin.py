from typing import List, Union
from .DicomScans import DicomScans

import uuid


class DigitalTwin:
    def __init__(self,
                 age: int,
                 sex: str,
                 firstname: str,
                 lastname: str,
                 user_uuid: Union[str, None] = None,
                 conditions: List[str] = [],
                 dicom_scans: DicomScans = DicomScans(),
                 models: List = []
                 ) -> None:
        self.uuid: str = user_uuid if user_uuid is not None else str(uuid.uuid4())
        self.age: int = age
        self.sex: str = sex
        self.firstname: str = firstname
        self.lastname: str = lastname
        self.conditions: List[str] = conditions
        self.dicom_scans: DicomScans = dicom_scans
        self.models = models

    def update_twin_info(self):
        pass
