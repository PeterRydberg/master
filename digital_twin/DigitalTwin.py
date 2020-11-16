from typing import List, Union
from .DicomScans import DicomScans

import uuid as uuid_getter


class DigitalTwin:
    def __init__(self,
                 age: int,
                 sex: str,
                 firstname: str,
                 lastname: str,
                 uuid: Union[str, None] = None,
                 conditions: List[str] = [],
                 dicom_scans: DicomScans = DicomScans(),
                 models: List = []
                 ) -> None:
        self.uuid: str = uuid if uuid is not None else str(uuid_getter.uuid4())
        self.age: int = age
        self.sex: str = sex
        self.firstname: str = firstname
        self.lastname: str = lastname
        self.conditions: List[str] = conditions
        self.dicom_scans: DicomScans = dicom_scans
        self.models = models

    def update_twin_info(self):
        pass
