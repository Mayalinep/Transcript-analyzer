import logging
import sys
from pathlib import Path

def setup_logging(debug: bool = False, log_file: str = None):
    """Configure le système de logging.
    
    Args:
        debug (bool): Si True, active le mode debug avec plus de logs
        log_file (str): Chemin vers le fichier de log (optionnel)
    """
    # Niveau de log
    log_level = logging.DEBUG if debug else logging.INFO
    
    # Format des logs
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Configuration de base
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt=date_format,
        handlers=[]
    )
    
    # Handler pour la console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(log_format, date_format))
    logging.getLogger().addHandler(console_handler)
    
    # Handler pour le fichier si spécifié
    if log_file:
        # Crée le répertoire des logs si nécessaire
        log_dir = Path(log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(logging.Formatter(log_format, date_format))
        logging.getLogger().addHandler(file_handler)
        
    logging.info("Système de logging initialisé") 