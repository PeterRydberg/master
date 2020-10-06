from typing import List
from Appendices import Appendices

import uuid


class DigitalTwin:
    def __init__(self,
                 age: int,
                 sex: str,
                 firstname: str,
                 lastname: str,
                 conditions: List[str] = [],
                 appendices: Appendices = Appendices()
                 ) -> None:
        self.uuid: str = str(uuid.uuid4())
        self.age: int = age
        self.sex: str = sex
        self.firstname: str = firstname
        self.lastname: str = lastname
        self.conditions: List[str] = conditions
        self.appendices: Appendices = appendices
        self.models = []
