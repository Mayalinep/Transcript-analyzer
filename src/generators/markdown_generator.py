import logging
import time
from typing import Dict
from pathlib import Path
from ..analyzers.base import TextAnalyzer
from ..analyzers.basic_analyzer import BasicAnalyzer
from ..analyzers.openai_analyzer import OpenAIAnalyzer
from ..analyzers.huggingface_analyzer import HuggingFaceAnalyzer

class DocumentGenerator:
    """Classe pour générer la documentation Markdown"""
    
    def __init__(self, analyzer: TextAnalyzer):
        self.analyzer = analyzer

    def generate_markdown(self, transcript_path: str, output_path: str):
        """Génère un document Markdown à partir de la transcription."""
        try:
            with open(transcript_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            logging.info("Nettoyage du texte...")
            cleaned_text = self.analyzer.clean_text(text)
            
            logging.info("Extraction des sections...")
            sections = self.analyzer.extract_sections(cleaned_text)
            
            logging.info("Création du résumé...")
            summary = self.analyzer.create_summary(cleaned_text)
            
            logging.info("Génération du document Markdown...")
            markdown = self._create_markdown_content(summary, sections)
            
            # Crée le répertoire de sortie si nécessaire
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown)
                
            logging.info(f"Documentation générée avec succès : {output_path}")
            
        except Exception as e:
            logging.error(f"Erreur lors de la génération de la documentation : {str(e)}")
            raise

    def _create_markdown_content(self, summary: str, sections: Dict[str, str]) -> str:
        """Crée le contenu Markdown."""
        # Détermine le type d'analyseur utilisé
        analyzer_type = "basique"
        if isinstance(self.analyzer, HuggingFaceAnalyzer):
            analyzer_type = "Hugging Face"
        elif isinstance(self.analyzer, OpenAIAnalyzer):
            analyzer_type = "OpenAI"

        markdown = f"""# Analyse de la Transcription

## Méthode d'analyse
Cette analyse a été générée en utilisant l'analyseur **{analyzer_type}**.

## Résumé
{summary}

## Table des Matières
1. [Introduction](#introduction)
2. [Installation et Configuration](#installation-et-configuration)
3. [Fonctionnalités](#fonctionnalités)
4. [Utilisation](#utilisation)
5. [Conclusion](#conclusion)

"""
        for title, content in sections.items():
            if content.strip():
                # Convertit le titre en ancre valide pour le lien
                anchor = title.lower().replace(' ', '-').replace('é', 'e')
                markdown += f"## {title}\n{content}\n\n"

        markdown += f"""---
Généré automatiquement à partir de la transcription
Méthode d'analyse : {analyzer_type}
Date de génération : {time.strftime('%Y-%m-%d %H:%M:%S')}
---"""

        return markdown 