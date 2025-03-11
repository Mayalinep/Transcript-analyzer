import os
import logging
import argparse
from pathlib import Path
from typing import Optional

from .analyzers.basic_analyzer import BasicAnalyzer
from .analyzers.openai_analyzer import OpenAIAnalyzer, OPENAI_AVAILABLE
from .analyzers.huggingface_analyzer import HuggingFaceAnalyzer, HUGGING_FACE_AVAILABLE
from .generators.markdown_generator import DocumentGenerator
from .utils.logging_config import setup_logging

def get_analyzer(analyzer_type: str = "basic", openai_api_key: Optional[str] = None):
    """Retourne l'analyseur approprié selon le type demandé."""
    logging.info(f"Initialisation de l'analyseur de type '{analyzer_type}'")
    
    if analyzer_type == "openai":
        if not OPENAI_AVAILABLE:
            logging.error("OpenAI n'est pas installé. Installation avec 'pip install openai' requise.")
            logging.info("Utilisation de l'analyseur basique comme fallback")
            return BasicAnalyzer()
        
        if not openai_api_key:
            logging.error("Clé API OpenAI manquante. Une clé valide est requise pour utiliser l'analyseur OpenAI.")
            logging.info("Utilisation de l'analyseur basique comme fallback")
            return BasicAnalyzer()
        
        try:
            return OpenAIAnalyzer(openai_api_key)
        except Exception as e:
            logging.error(f"Erreur lors de l'initialisation de l'analyseur OpenAI: {str(e)}")
            logging.info("Utilisation de l'analyseur basique comme fallback")
            return BasicAnalyzer()
            
    elif analyzer_type == "huggingface":
        if not HUGGING_FACE_AVAILABLE:
            logging.error("Hugging Face n'est pas installé. Installation avec 'pip install transformers' requise.")
            logging.info("Utilisation de l'analyseur basique comme fallback")
            return BasicAnalyzer()
        
        try:
            return HuggingFaceAnalyzer()
        except Exception as e:
            logging.error(f"Erreur lors de l'initialisation de l'analyseur Hugging Face: {str(e)}")
            logging.info("Utilisation de l'analyseur basique comme fallback")
            return BasicAnalyzer()
    
    logging.info("Utilisation de l'analyseur basique")
    return BasicAnalyzer()

def main():
    parser = argparse.ArgumentParser(description="Analyse une transcription et génère une documentation Markdown")
    parser.add_argument("--analyzer", choices=["basic", "huggingface", "openai"], default="basic",
                      help="Type d'analyseur à utiliser")
    parser.add_argument("--openai-key", help="Clé API OpenAI (requise pour l'analyseur OpenAI)")
    parser.add_argument("--debug", action="store_true", help="Active le mode debug avec plus de logs")
    parser.add_argument("--log-file", help="Fichier de log (optionnel)")
    args = parser.parse_args()

    # Configuration du logging
    setup_logging(args.debug, args.log_file)
    
    try:
        if not os.path.exists('transcriptions'):
            logging.error("Le dossier 'transcriptions' n'existe pas.")
            return
        
        transcription_files = [f for f in os.listdir('transcriptions') if f.endswith('_transcription.txt')]
        if not transcription_files:
            logging.error("Aucun fichier de transcription trouvé.")
            return
            
        latest_transcription = max(transcription_files, key=lambda x: os.path.getctime(os.path.join('transcriptions', x)))
        transcript_path = os.path.join('transcriptions', latest_transcription)
        logging.debug(f"Fichier de transcription sélectionné : {transcript_path}")
        
        analyzer_suffix = f"_{args.analyzer}"
        output_filename = latest_transcription.replace('_transcription.txt', f'{analyzer_suffix}_analysis.md')
        output_path = os.path.join('transcriptions', output_filename)
        logging.debug(f"Fichier de sortie : {output_path}")
        
        analyzer = get_analyzer(args.analyzer, args.openai_key)
        generator = DocumentGenerator(analyzer)
        generator.generate_markdown(transcript_path, output_path)
        
        logging.info(f"Documentation générée avec l'analyseur {args.analyzer}")
        
    except Exception as e:
        logging.error(f"Erreur lors de la génération de la documentation : {str(e)}")
        if args.debug:
            import traceback
            logging.debug("Stacktrace complète :")
            logging.debug(traceback.format_exc())

if __name__ == "__main__":
    main() 