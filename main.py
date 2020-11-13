from digital_twin.DigitalTwinPopulation import DigitalTwinPopulation
from knowledge_bank.KnowledgeBank import KnowledgeBank
from knowledge_generation_engine.KnowledgeGenerationEngine import KnowledgeGenerationEngine

if __name__ == "__main__":
    #dts = DigitalTwinPopulation()
    # dts.generate_new_population(size=100)
    kge = KnowledgeGenerationEngine(
        dicom_type="prostate",
        knowledge_bank=KnowledgeBank())
    kge.update_virtual_registry()
