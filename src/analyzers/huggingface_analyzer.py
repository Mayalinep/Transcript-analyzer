import logging
from typing import Dict
from .base import TextAnalyzer
from .basic_analyzer import BasicAnalyzer

try:
    from transformers import pipeline
    HUGGING_FACE_AVAILABLE = True
    logging.info("Hugging Face est disponible")
except ImportError as e:
    HUGGING_FACE_AVAILABLE = False
    logging.error(f"Erreur d'importation Hugging Face: {str(e)}")

class HuggingFaceAnalyzer(TextAnalyzer):
    """Analyseur de texte utilisant les modèles Hugging Face"""
    
    def __init__(self):
        self.models_loaded = False
        if not HUGGING_FACE_AVAILABLE:
            logging.error("Hugging Face n'est pas disponible, utilisation de l'analyseur basique")
            self.fallback = BasicAnalyzer()
            return
        
        try:
            logging.info("Initialisation des modèles Hugging Face...")
            
            # Modèle BART français pour le résumé
            self.summarizer = pipeline(
                "summarization",
                model="moussaKam/barthez-orangesum-title",
                device=-1  # Force CPU
            )
            
            # Modèle CamemBERT pour la classification
            self.classifier = pipeline(
                "text-classification",
                model="dbmdz/bert-base-french-europeana-cased",
                device=-1  # Force CPU
            )
            
            self.models_loaded = True
            logging.info("Modèles Hugging Face initialisés avec succès")
        except Exception as e:
            logging.error(f"Erreur lors de l'initialisation des modèles Hugging Face: {str(e)}")
            self.fallback = BasicAnalyzer()

    def clean_text(self, text: str) -> str:
        """Nettoie le texte."""
        if not self.models_loaded:
            return self.fallback.clean_text(text)
            
        try:
            logging.info("Nettoyage du texte avec Hugging Face...")
            # Utilise le modèle CamemBERT pour identifier les parties importantes
            chunks = [text[i:i + 512] for i in range(0, len(text), 512)]
            cleaned_chunks = []
            
            for chunk in chunks:
                # Classifie l'importance du chunk
                result = self.classifier(chunk)
                if result[0]['score'] > 0.5:  # Si le chunk est considéré comme important
                    cleaned_chunks.append(chunk)
            
            cleaned_text = " ".join(cleaned_chunks)
            logging.info("Texte nettoyé avec succès")
            return cleaned_text
        except Exception as e:
            logging.error(f"Erreur lors du nettoyage du texte avec Hugging Face: {str(e)}")
            return self.fallback.clean_text(text)

    def create_summary(self, text: str, max_length: int = 1500) -> str:
        """Crée un résumé avec le modèle BART."""
        if not self.models_loaded:
            return self.fallback.create_summary(text, max_length)
            
        try:
            logging.info("Création du résumé avec Hugging Face...")
            # Découpe le texte en morceaux de 512 tokens maximum
            chunks = [text[i:i + 512] for i in range(0, len(text), 512)]
            summaries = []
            
            for chunk in chunks:
                summary = self.summarizer(
                    chunk,
                    max_length=150,
                    min_length=40,
                    do_sample=False
                )[0]['summary_text']
                summaries.append(summary)
            
            final_summary = " ".join(summaries)
            if len(final_summary) > max_length:
                final_summary = final_summary[:max_length] + "..."
                
            logging.info("Résumé créé avec succès")
            return final_summary
            
        except Exception as e:
            logging.error(f"Erreur lors de la génération du résumé avec Hugging Face: {str(e)}")
            return self.fallback.create_summary(text, max_length)

    def extract_sections(self, text: str) -> Dict[str, str]:
        """Extrait les sections avec classification."""
        if not self.models_loaded:
            return self.fallback.extract_sections(text)
            
        try:
            logging.info("Extraction des sections avec Hugging Face...")
            sections = {
                "Introduction": "",
                "Installation et Configuration": "",
                "Fonctionnalités": "",
                "Utilisation": "",
                "Conclusion": ""
            }
            
            # Découpe le texte en paragraphes
            paragraphs = text.split('\n\n')
            
            for para in paragraphs:
                if not para.strip():
                    continue
                
                # Classifie le paragraphe
                result = self.classifier(para[:512])  # Limite la taille pour éviter les dépassements
                score = result[0]['score']
                
                # Détermine la section appropriée basée sur des mots-clés
                if "introduction" in para.lower() or "contexte" in para.lower():
                    sections["Introduction"] += para + "\n\n"
                elif "install" in para.lower() or "config" in para.lower():
                    sections["Installation et Configuration"] += para + "\n\n"
                elif "fonction" in para.lower() or "caractéristique" in para.lower():
                    sections["Fonctionnalités"] += para + "\n\n"
                elif "utilis" in para.lower() or "exemple" in para.lower():
                    sections["Utilisation"] += para + "\n\n"
                elif "conclu" in para.lower() or "synthèse" in para.lower():
                    sections["Conclusion"] += para + "\n\n"
                else:
                    # Si le score est élevé, met dans Introduction
                    if score > 0.8:
                        sections["Introduction"] += para + "\n\n"
                    # Sinon, met dans la section la plus appropriée basée sur la position
                    else:
                        position = len(para) / len(text)
                        if position < 0.2:
                            sections["Introduction"] += para + "\n\n"
                        elif position < 0.4:
                            sections["Installation et Configuration"] += para + "\n\n"
                        elif position < 0.6:
                            sections["Fonctionnalités"] += para + "\n\n"
                        elif position < 0.8:
                            sections["Utilisation"] += para + "\n\n"
                        else:
                            sections["Conclusion"] += para + "\n\n"
            
            # Améliore chaque section avec le résumé
            for section_name, content in sections.items():
                if content.strip():
                    try:
                        summary = self.summarizer(
                            content[:512],
                            max_length=200,
                            min_length=50
                        )[0]['summary_text']
                        sections[section_name] = summary + "\n\n" + content
                        logging.info(f"Section '{section_name}' améliorée avec succès")
                    except Exception as e:
                        logging.error(f"Erreur lors de l'amélioration de la section '{section_name}': {str(e)}")
            
            logging.info("Extraction des sections terminée avec succès")
            return sections
            
        except Exception as e:
            logging.error(f"Erreur lors de l'extraction des sections avec Hugging Face: {str(e)}")
            return self.fallback.extract_sections(text) 