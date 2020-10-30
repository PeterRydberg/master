class KnowledgeBank:
    def __init__(self) -> None:
        self.models = {}

    def infer(self, model, data):
        pass

    def update_model(self, dicom_type, model):
        self.models[dicom_type] = model
