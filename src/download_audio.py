import os
import logging
from pathlib import Path
import yt_dlp

def download_audio(url: str, output_dir: str = "downloads") -> str:
    """
    Télécharge l'audio d'une vidéo YouTube.
    
    Args:
        url: URL de la vidéo YouTube
        output_dir: Dossier de sortie pour l'audio
    
    Returns:
        Chemin vers le fichier audio téléchargé
    """
    try:
        # Crée le dossier de sortie s'il n'existe pas
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Configuration de yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True
        }
        
        logging.info(f"Téléchargement de l'audio depuis : {url}")
        
        # Télécharge l'audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            audio_path = os.path.join(output_dir, f"{info['title']}.wav")
            
        logging.info(f"Audio téléchargé avec succès : {audio_path}")
        return audio_path
        
    except Exception as e:
        logging.error(f"Erreur lors du téléchargement de l'audio : {str(e)}")
        raise

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Télécharge l'audio d'une vidéo YouTube")
    parser.add_argument("url", help="URL de la vidéo YouTube")
    parser.add_argument("--output-dir", default="downloads", help="Dossier de sortie pour l'audio")
    args = parser.parse_args()
    
    try:
        audio_path = download_audio(args.url, args.output_dir)
        print(f"Audio téléchargé : {audio_path}")
    except Exception as e:
        print(f"Erreur : {str(e)}")
        exit(1) 