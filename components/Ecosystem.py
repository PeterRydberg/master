from components.digital_twin.DigitalTwinPopulation import DigitalTwinPopulation
from components.knowledge_generation_engine.KnowledgeGenerationEngine import KnowledgeGenerationEngine
from components.knowledge_bank.KnowledgeBank import KnowledgeBank


class Ecosystem:
    def __init__(self) -> None:
        self.digital_twin_population: DigitalTwinPopulation = DigitalTwinPopulation(self)
        self.knowledge_generation_engine: KnowledgeGenerationEngine = KnowledgeGenerationEngine(self)
        self.knowledge_bank: KnowledgeBank = KnowledgeBank(self)
