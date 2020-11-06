from knowledge_bank.KnowledgeBank import KnowledgeBank
from knowledge_generation_engine.KnowledgeGenerationEngine import KnowledgeGenerationEngine

if __name__ == "__main__":
    kge = KnowledgeGenerationEngine(
        dicom_type="prostate",
        knowledge_bank=KnowledgeBank())
    kge.update_virtual_registry()
