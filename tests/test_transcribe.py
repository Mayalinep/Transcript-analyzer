import unittest
import os
from src.transcribe_audio import transcribe_audio

class TestTranscribeAudio(unittest.TestCase):
    def setUp(self):
        """Initialise l'environnement de test."""
        self.test_audio = "test_audio.wav"
        self.test_output_dir = "test_transcriptions"
        
        # Crée un fichier audio de test vide
        with open(self.test_audio, "wb") as f:
            f.write(b"")
            
    def tearDown(self):
        """Nettoie l'environnement après les tests."""
        if os.path.exists(self.test_audio):
            os.remove(self.test_audio)
        if os.path.exists(self.test_output_dir):
            for file in os.listdir(self.test_output_dir):
                os.remove(os.path.join(self.test_output_dir, file))
            os.rmdir(self.test_output_dir)

    def test_transcribe_audio_creates_directory(self):
        """Teste que le dossier de sortie est créé."""
        try:
            transcribe_audio(self.test_audio, self.test_output_dir)
        except:
            pass  # On ignore les erreurs de transcription
        self.assertTrue(os.path.exists(self.test_output_dir))

    def test_transcribe_audio_invalid_file(self):
        """Teste la gestion des fichiers audio invalides."""
        with self.assertRaises(Exception):
            transcribe_audio("invalid_file.wav", self.test_output_dir)

if __name__ == '__main__':
    unittest.main() 