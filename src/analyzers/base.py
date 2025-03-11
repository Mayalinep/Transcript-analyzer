from abc import ABC, abstractmethod
from typing import Dict

class TextAnalyzer(ABC):
    """Classe abstraite pour l'analyse de texte"""
    
    @abstractmethod
    def clean_text(self, text: str) -> str:
        """Nettoie le texte en supprimant les répétitions et en améliorant la ponctuation."""
        pass

    @abstractmethod
    def create_summary(self, text: str, max_length: int = 1500) -> str:
        """Crée un résumé synthétique du texte."""
        pass

    @abstractmethod
    def extract_sections(self, text: str) -> Dict[str, str]:
        """Extrait les sections principales du texte."""
        pass 