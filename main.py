from digital_twin.DigitalTwinPopulation import DigitalTwinPopulation
from knowledge_bank.KnowledgeBank import KnowledgeBank
from knowledge_generation_engine.KnowledgeGenerationEngine import KnowledgeGenerationEngine

if __name__ == "__main__":
    dtp = DigitalTwinPopulation()
    kb = KnowledgeBank()
    kge = KnowledgeGenerationEngine(
        dicom_type="prostate"
    )

    kge.update_virtual_registry()
