from knowledge_bank.KnowledgeBank import KnowledgeBank
from knowledge_generation_engine.KnowledgeGenerationEngine import KnowledgeGenerationEngine

if __name__ == "__main__":
    kge = KnowledgeGenerationEngine(
        dicom_type="heart",
        virtual_register="register_heart",
        knowledge_bank=KnowledgeBank())
    kge.update_virtual_registry()
