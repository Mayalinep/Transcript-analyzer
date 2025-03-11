import re
from typing import Dict
from .base import TextAnalyzer

class BasicAnalyzer(TextAnalyzer):
    """Analyseur de texte basique sans IA"""
    
    def clean_text(self, text: str) -> str:
        """Nettoie le texte en supprimant les répétitions et en améliorant la ponctuation."""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'([a-zA-Z])\s+([A-Z])', r'\1. \2', text)
        return text.strip()

    def create_summary(self, text: str, max_length: int = 1500) -> str:
        """Crée un résumé synthétique du texte."""
        sentences = re.split(r'[.!?]+', text)
        important_sentences = []
        
        keywords = ["important", "clé", "essentiel", "principal", "permet", "fonction", "capable"]
        
        for sentence in sentences:
            sentence = sentence.strip()
            if any(keyword in sentence.lower() for keyword in keywords) and len(sentence) > 20:
                important_sentences.append(sentence)
        
        summary = ". ".join(important_sentences[:5])
        if len(summary) > max_length:
            summary = summary[:max_length] + "..."
        
        return summary

    def extract_sections(self, text: str) -> Dict[str, str]:
        """Extrait les sections du texte."""
        sections = {
            "Introduction": "",
            "Installation et Configuration": "",
            "Fonctionnalités": "",
            "Utilisation": "",
            "Conclusion": ""
        }
        
        paragraphs = text.split('\n\n')
        current_section = "Introduction"
        
        for para in paragraphs:
            if any(word in para.lower() for word in ["installer", "télécharger", "configuration", "setup"]):
                current_section = "Installation et Configuration"
            elif any(word in para.lower() for word in ["fonctionnalité", "capable", "permet"]):
                current_section = "Fonctionnalités"
            elif any(word in para.lower() for word in ["utiliser", "exemple", "comment"]):
                current_section = "Utilisation"
            elif any(word in para.lower() for word in ["conclusion", "finalement", "bref"]):
                current_section = "Conclusion"
                
            sections[current_section] += para + "\n\n"
        
        return sections 