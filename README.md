# Analyseur de Transcriptions

Solution tout-en-un pour transformer vos vidéos YouTube en documentation structurée. Cet outil combine :
- 🎥 Téléchargement automatique de vidéos YouTube
- 🎙️ Transcription audio de haute qualité avec Whisper
- 🤖 Analyse intelligente du texte avec des modèles IA
- 📚 Génération de documentation claire et structurée
- 🇫🇷 Optimisation complète pour le français

## 🚀 Fonctionnalités

- Téléchargement de vidéos YouTube en audio
- Transcription audio en texte avec Whisper
- Analyse de transcriptions avec différents moteurs (Basic, OpenAI, Hugging Face)
- Génération automatique de résumés
- Extraction intelligente de sections
- Support multilingue (optimisé pour le français)

## 📋 Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- ffmpeg (pour le traitement audio)

## 💻 Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/Mayalinep/Transcript-analyzer.git
cd Transcript-analyzer
```

2. Créez un environnement virtuel :
```bash
python -m venv myenv
source myenv/bin/activate  # Sur Linux/Mac
# ou
myenv\Scripts\activate  # Sur Windows
```

3. Installez le package :
```bash
pip install -e ".[huggingface]"  # Installation avec toutes les fonctionnalités
```

## 🎯 Utilisation

Le processus se fait en 3 étapes :

### 1. Télécharger une vidéo YouTube
```bash
python src/download_audio.py "URL_YOUTUBE"
```
Cela télécharge l'audio dans le dossier `downloads/`

### 2. Transcrire l'audio
```bash
python src/transcribe_audio.py "downloads/nom_du_fichier.wav"
```
Cela génère la transcription dans le dossier `transcriptions/`

### 3. Analyser la transcription
```bash
analyze-transcript --analyzer huggingface --debug
```
Cela crée un fichier Markdown avec l'analyse dans `transcriptions/`

### Options d'analyse disponibles :
- `--analyzer` : Choisir le moteur d'analyse (par défaut: basic)
  - `basic` : Analyse simple sans IA
  - `huggingface` : Utilise des modèles français de Hugging Face
  - `openai` : Utilise GPT d'OpenAI (nécessite une clé API)
- `--debug` : Activer les logs détaillés

## 🔧 Configuration des analyseurs

### Hugging Face
- Aucune configuration supplémentaire requise
- Utilise des modèles français par défaut :
  - BART pour les résumés
  - CamemBERT pour la classification

### OpenAI (optionnel)
- Nécessite une clé API OpenAI
- Configurez la variable d'environnement :
```bash
export OPENAI_API_KEY="votre-clé-api"
```

## 📝 Format de sortie

L'analyseur génère un fichier Markdown structuré avec :
- Un résumé global
- Des sections organisées (Introduction, Installation, etc.)
- Une mise en forme optimisée pour la lecture

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Soumettre des pull requests

## 📄 Licence

Ce projet est sous licence Creative Commons Attribution-NonCommercial 4.0 (CC BY-NC 4.0). Cela signifie que vous pouvez :
- Partager et modifier le code
- Utiliser le projet pour un usage personnel
- Distribuer vos modifications

Mais vous ne pouvez pas :
- Utiliser le projet à des fins commerciales

Vous devez :
- Créditer le projet original
- Indiquer les modifications apportées

Voir le fichier `LICENSE` pour plus de détails. 