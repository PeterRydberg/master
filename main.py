from digital_twin.DigitalTwinPopulation import DigitalTwinPopulation
from knowledge_bank.KnowledgeBank import KnowledgeBank
from knowledge_generation_engine.KnowledgeGenerationEngine import KnowledgeGenerationEngine

if __name__ == "__main__":
    kge = KnowledgeGenerationEngine(
        dicom_type="prostate",
        knowledge_bank=KnowledgeBank())
    kge.update_virtual_registry()
    dts = DigitalTwinPopulation()
    dts.get_user_by_id("d91ea28a-e8e6-429e-8297-ce104ebdc772")
