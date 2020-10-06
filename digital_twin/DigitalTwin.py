from typing import List
from DicomScans import DicomScans

import uuid


class DigitalTwin:
    def __init__(self,
                 age: int,
                 sex: str,
                 firstname: str,
                 lastname: str,
                 conditions: List[str] = [],
                 dicom_scans: DicomScans = DicomScans()
                 ) -> None:
        self.uuid: str = str(uuid.uuid4())
        self.age: int = age
        self.sex: str = sex
        self.firstname: str = firstname
        self.lastname: str = lastname
        self.conditions: List[str] = conditions
        self.dicom_scans: DicomScans = dicom_scans
        self.models = []
