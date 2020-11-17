from digital_twin.DigitalTwinPopulation import DigitalTwinPopulation
from knowledge_bank.KnowledgeBank import KnowledgeBank
from knowledge_generation_engine.KnowledgeGenerationEngine import KnowledgeGenerationEngine

if __name__ == "__main__":
    dtp = DigitalTwinPopulation()
    kb = KnowledgeBank()
    kge = KnowledgeGenerationEngine()

    # dtp.generate_new_population(size=100)
    kge.update_virtual_register(image_type="prostate")
    # kb.process_new_images()

    # Tillat både segmentation og inferens (helst opprette nye modeller automatisk)
    # Sett opp Ecosystem.py
    # Tren automatisk
