import requests
import json
from typing import Optional, Dict, Any
from config import Config

class SarvamAIClient:
    """Client for interacting with Sarvam AI APIs"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.sarvam.ai"
        self.headers = {
            "api-subscription-key": api_key,
            "Content-Type": "application/json"
        }
    
    def detect_language(self, text: str) -> Optional[str]:
        """
        Detect the language of input text using Sarvam AI language detection
        """
        try:
            url = f"{self.base_url}/detect-language"
            payload = {"input": text}
            
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            detected_lang = result.get('language_code', 'en')
            
            # Map to our supported language codes
            lang_mapping = {
                'hin': 'hi',
                'ben': 'bn', 
                'tel': 'te',
                'tam': 'ta',
                'mar': 'mr',
                'guj': 'gu',
                'kan': 'kn',
                'mal': 'ml',
                'pan': 'pa',
                'ori': 'or',
                'eng': 'en'
            }
            
            return lang_mapping.get(detected_lang, 'en')
            
        except Exception as e:
            print(f"Language detection error: {e}")
            return 'en'  # Default to English
    
    def translate_text(self, text: str, target_language: str, source_language: str = "auto") -> Optional[str]:
        """
        Translate text using Sarvam AI translation API
        """
        try:
            url = f"{self.base_url}/translate"
            payload = {
                "input": text,
                "source_language_code": source_language,
                "target_language_code": Config.SUPPORTED_LANGUAGES.get(target_language, 'en-IN'),
                "speaker_gender": "Male",
                "mode": "formal",
                "model": "mayura:v1",
                "enable_preprocessing": True
            }
            
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            return result.get('translated_text', text)
            
        except Exception as e:
            print(f"Translation error: {e}")
            return text
    
    def speech_to_text(self, audio_file_path: str, language_code: str = "hi-IN") -> Optional[str]:
        """
        Convert speech to text using Sarvam AI ASR
        """
        try:
            url = f"{self.base_url}/speech-to-text"
            
            # Prepare multipart form data
            files = {
                'file': open(audio_file_path, 'rb')
            }
            
            data = {
                'model': 'saarika:v2',
                'language_code': Config.SUPPORTED_LANGUAGES.get(language_code, 'hi-IN')
            }
            
            # Remove Content-Type header for multipart/form-data
            headers = {"api-subscription-key": self.api_key}
            
            response = requests.post(url, headers=headers, files=files, data=data)
            response.raise_for_status()
            
            result = response.json()
            return result.get('transcript', '')
            
        except Exception as e:
            print(f"Speech to text error: {e}")
            return None
        finally:
            if 'files' in locals():
                files['file'].close()
    
    def text_to_speech(self, text: str, language_code: str = "hi-IN") -> Optional[bytes]:
        """
        Convert text to speech using Sarvam AI TTS
        """
        try:
            url = f"{self.base_url}/text-to-speech"
            payload = {
                "inputs": [text],
                "target_language_code": Config.SUPPORTED_LANGUAGES.get(language_code, 'hi-IN'),
                "speaker": "meera",
                "pitch": 0,
                "pace": 1.0,
                "loudness": 1.0,
                "speech_sample_rate": 8000,
                "enable_preprocessing": True,
                "model": "bulbul:v1"
            }
            
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            
            # Sarvam returns base64 encoded audio
            import base64
            if 'audios' in result and len(result['audios']) > 0:
                audio_base64 = result['audios'][0]
                return base64.b64decode(audio_base64)
            
            return None
            
        except Exception as e:
            print(f"Text to speech error: {e}")
            return None
    
    def speech_to_text_translate(self, audio_file_path: str, target_language: str = "en") -> Optional[str]:
        """
        Convert speech to text and translate to target language
        """
        try:
            url = f"{self.base_url}/speech-to-text-translate"
            
            files = {
                'file': open(audio_file_path, 'rb')
            }
            
            data = {
                'model': 'saaras:v1',
                'target_language_code': Config.SUPPORTED_LANGUAGES.get(target_language, 'en-IN')
            }
            
            headers = {"api-subscription-key": self.api_key}
            
            response = requests.post(url, headers=headers, files=files, data=data)
            response.raise_for_status()
            
            result = response.json()
            return result.get('translated_text', '')
            
        except Exception as e:
            print(f"Speech to text translate error: {e}")
            return None
        finally:
            if 'files' in locals():
                files['file'].close() 