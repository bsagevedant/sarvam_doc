import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for the multilingual AI doctor agent"""
    
    SARVAM_API_KEY = os.getenv('SARVAM_API_KEY')
    PORT = int(os.getenv('PORT', 5001))
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # Supported languages mapping
    SUPPORTED_LANGUAGES = {
        'hi': 'hi-IN',  # Hindi
        'bn': 'bn-IN',  # Bengali
        'te': 'te-IN',  # Telugu
        'ta': 'ta-IN',  # Tamil
        'mr': 'mr-IN',  # Marathi
        'gu': 'gu-IN',  # Gujarati
        'kn': 'kn-IN',  # Kannada
        'ml': 'ml-IN',  # Malayalam
        'pa': 'pa-IN',  # Punjabi
        'or': 'or-IN',  # Odia
        'en': 'en-IN'   # English
    }
    
    # Language display names
    LANGUAGE_NAMES = {
        'hi': 'हिंदी',
        'bn': 'বাংলা',
        'te': 'తెలుగు',
        'ta': 'தமிழ்',
        'mr': 'मराठी',
        'gu': 'ગુજરાતી',
        'kn': 'ಕನ್ನಡ',
        'ml': 'മലയാളം',
        'pa': 'ਪੰਜਾਬੀ',
        'or': 'ଓଡ଼ିଆ',
        'en': 'English'
    }
    
    # Medical consultation system prompt
    MEDICAL_PROMPT_TEMPLATE = """You are Dr. Sarvam, a helpful and knowledgeable AI medical assistant. You provide medical guidance in a compassionate and professional manner.

IMPORTANT GUIDELINES:
1. Always ask follow-up questions to understand symptoms better
2. Provide general medical advice but always recommend consulting a qualified doctor
3. Be culturally sensitive and respectful
4. Use simple, easy-to-understand language
5. If symptoms are severe, immediately advise visiting emergency services
6. Do not provide specific medication dosages or prescriptions
7. Focus on preventive care and general wellness advice

Patient Query: {query}
Detected Language: {language}

Please respond in {language_name} language with:
1. Understanding of the symptoms
2. General advice and possible causes
3. When to seek immediate medical attention
4. Follow-up questions to better understand the condition
5. General preventive measures

Remember to be empathetic and professional while maintaining medical accuracy.""" 