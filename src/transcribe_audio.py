import os
import logging
from pathlib import Path
import whisper

def transcribe_audio(audio_path: str, output_dir: str = "transcriptions", model_name: str = "base") -> str:
    """
    Transcrit un fichier audio en texte.
    
    Args:
        audio_path: Chemin vers le fichier audio
        output_dir: Dossier de sortie pour la transcription
        model_name: Nom du modèle Whisper à utiliser
    
    Returns:
        Chemin vers le fichier de transcription
    """
    try:
        # Crée le dossier de sortie s'il n'existe pas
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Charge le modèle Whisper
        logging.info(f"Chargement du modèle Whisper '{model_name}'")
        model = whisper.load_model(model_name)
        
        # Transcrit l'audio
        logging.info(f"Transcription de l'audio : {audio_path}")
        result = model.transcribe(audio_path, language="fr")
        
        # Génère le nom du fichier de sortie
        base_name = os.path.splitext(os.path.basename(audio_path))[0]
        output_path = os.path.join(output_dir, f"{base_name}_transcription.txt")
        
        # Sauvegarde la transcription
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result["text"])
            
        logging.info(f"Transcription sauvegardée : {output_path}")
        return output_path
        
    except Exception as e:
        logging.error(f"Erreur lors de la transcription : {str(e)}")
        raise

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Transcrit un fichier audio en texte")
    parser.add_argument("audio_path", help="Chemin vers le fichier audio")
    parser.add_argument("--output-dir", default="transcriptions", help="Dossier de sortie pour la transcription")
    parser.add_argument("--model", default="base", help="Modèle Whisper à utiliser")
    args = parser.parse_args()
    
    try:
        transcript_path = transcribe_audio(args.audio_path, args.output_dir, args.model)
        print(f"Transcription générée : {transcript_path}")
    except Exception as e:
        print(f"Erreur : {str(e)}")
        exit(1) 