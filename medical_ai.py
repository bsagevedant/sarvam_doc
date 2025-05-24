import re
from typing import Dict, List, Optional, Tuple
from config import Config

class MedicalAI:
    """Medical AI consultation system"""
    
    def __init__(self):
        self.medical_knowledge = self._load_medical_knowledge()
        self.symptom_patterns = self._load_symptom_patterns()
        self.emergency_keywords = [
            'chest pain', 'difficulty breathing', 'unconscious', 'severe bleeding',
            'heart attack', 'stroke', 'poisoning', 'emergency', 'urgent',
            'सीने में दर्द', 'सांस लेने में तकलीफ', 'बेहोशी', 'खून बहना',
            'हार्ट अटैक', 'स्ट्रोक', 'इमरजेंसी', 'जरूरी', 'तुरंत'
        ]
    
    def _load_medical_knowledge(self) -> Dict:
        """Load medical knowledge base"""
        return {
            'fever': {
                'symptoms': ['high temperature', 'chills', 'sweating', 'headache'],
                'causes': ['viral infection', 'bacterial infection', 'immune response'],
                'advice': 'Rest, stay hydrated, take paracetamol if needed',
                'emergency': 'Fever above 103°F or lasting more than 3 days'
            },
            'headache': {
                'symptoms': ['head pain', 'pressure', 'throbbing'],
                'causes': ['stress', 'dehydration', 'sleep deprivation', 'migraine'],
                'advice': 'Rest in dark room, stay hydrated, gentle head massage',
                'emergency': 'Sudden severe headache, vision changes, or neck stiffness'
            },
            'cough': {
                'symptoms': ['persistent coughing', 'throat irritation', 'phlegm'],
                'causes': ['cold', 'allergies', 'respiratory infection'],
                'advice': 'Stay hydrated, honey and warm water, avoid irritants',
                'emergency': 'Coughing blood or severe breathing difficulty'
            },
            'stomach_pain': {
                'symptoms': ['abdominal pain', 'nausea', 'cramping'],
                'causes': ['indigestion', 'food poisoning', 'stress', 'gastritis'],
                'advice': 'Light diet, avoid spicy foods, stay hydrated',
                'emergency': 'Severe pain, vomiting blood, or high fever'
            },
            'cold': {
                'symptoms': ['runny nose', 'sneezing', 'sore throat', 'congestion'],
                'causes': ['viral infection', 'weakened immunity'],
                'advice': 'Rest, warm liquids, steam inhalation, vitamin C',
                'emergency': 'High fever or difficulty breathing'
            }
        }
    
    def _load_symptom_patterns(self) -> Dict:
        """Load symptom detection patterns"""
        return {
            'fever': [
                r'fever|temperature|बुखार|ज्वर|तापमान',
                r'hot|burning|गर्म|जलन'
            ],
            'headache': [
                r'headache|head.*pain|सिरदर्द|सिर.*दर्द',
                r'migraine|माइग्रेन'
            ],
            'cough': [
                r'cough|coughing|खांसी|कफ',
                r'throat.*pain|गले.*दर्द'
            ],
            'stomach_pain': [
                r'stomach.*pain|belly.*pain|पेट.*दर्द|उदर.*दर्द',
                r'nausea|vomit|उल्टी|मतली'
            ],
            'cold': [
                r'cold|runny.*nose|नाक.*बहना|जुकाम|सर्दी',
                r'sneezing|छींक|नाक.*जाम'
            ]
        }
    
    def detect_symptoms(self, query: str) -> List[str]:
        """Detect symptoms from user query"""
        query_lower = query.lower()
        detected_symptoms = []
        
        for symptom, patterns in self.symptom_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower, re.IGNORECASE):
                    detected_symptoms.append(symptom)
                    break
        
        return detected_symptoms
    
    def check_emergency(self, query: str) -> bool:
        """Check if query indicates emergency situation"""
        query_lower = query.lower()
        for keyword in self.emergency_keywords:
            if keyword.lower() in query_lower:
                return True
        return False
    
    def generate_medical_response(self, query: str, detected_language: str) -> str:
        """Generate medical response based on query and detected symptoms"""
        
        # Check for emergency
        if self.check_emergency(query):
            return self._generate_emergency_response(detected_language)
        
        # Detect symptoms
        symptoms = self.detect_symptoms(query)
        
        if not symptoms:
            return self._generate_general_response(query, detected_language)
        
        # Generate response for detected symptoms
        return self._generate_symptom_response(symptoms, detected_language)
    
    def _generate_emergency_response(self, language: str) -> str:
        """Generate emergency response"""
        responses = {
            'en': """🚨 MEDICAL EMERGENCY DETECTED 🚨

Please seek immediate medical attention:
• Call emergency services (108/102)
• Visit the nearest hospital emergency room
• Do not delay medical care

If this is a life-threatening emergency, please hang up and call emergency services immediately.

Stay calm and get professional medical help right away.""",
            
            'hi': """🚨 चिकित्सा आपातकाल का पता चला 🚨

कृपया तुरंत चिकित्सा सहायता लें:
• आपातकालीन सेवाओं को कॉल करें (108/102)
• निकटतम अस्पताल के आपातकालीन कक्ष में जाएं
• चिकित्सा देखभाल में देरी न करें

यदि यह जीवन-घातक आपातकाल है, तो कृपया फोन रखें और तुरंत आपातकालीन सेवाओं को कॉल करें।

शांत रहें और तुरंत पेशेवर चिकित्सा सहायता लें।"""
        }
        
        return responses.get(language, responses['en'])
    
    def _generate_general_response(self, query: str, language: str) -> str:
        """Generate general medical response"""
        responses = {
            'en': f"""Hello! I'm Dr. Sarvam, your AI medical assistant. I'm here to help you with your health concerns.

I understand you're asking about: "{query}"

To provide you with the best possible guidance, could you please tell me:
1. What specific symptoms are you experiencing?
2. How long have you been experiencing these symptoms?
3. Is there any particular area of concern?

Remember: I can provide general medical information and guidance, but I always recommend consulting with a qualified healthcare professional for proper diagnosis and treatment.

How can I help you today?""",
            
            'hi': f"""नमस्ते! मैं डॉ. सर्वम हूं, आपका AI चिकित्सा सहायक। मैं आपकी स्वास्थ्य समस्याओं में आपकी मदद के लिए यहां हूं।

मैं समझता हूं कि आप पूछ रहे हैं: "{query}"

आपको सबसे अच्छा मार्गदर्शन प्रदान करने के लिए, कृपया मुझे बताएं:
1. आप किन विशिष्ट लक्षणों का अनुभव कर रहे हैं?
2. आप कितने समय से इन लक्षणों का अनुभव कर रहे हैं?
3. क्या कोई विशेष चिंता का क्षेत्र है?

याद रखें: मैं सामान्य चिकित्सा जानकारी और मार्गदर्शन प्रदान कर सकता हूं, लेकिन मैं हमेशा उचित निदान और उपचार के लिए एक योग्य स्वास्थ्य सेवा पेशेवर से परामर्श करने की सलाह देता हूं।

आज मैं आपकी कैसे मदद कर सकता हूं?"""
        }
        
        return responses.get(language, responses['en'])
    
    def _generate_symptom_response(self, symptoms: List[str], language: str) -> str:
        """Generate response for specific symptoms"""
        
        # Take the first detected symptom for primary response
        primary_symptom = symptoms[0]
        symptom_info = self.medical_knowledge.get(primary_symptom, {})
        
        if language == 'hi':
            return f"""नमस्ते! मैं डॉ. सर्वम हूं। मैं समझता हूं कि आप {primary_symptom} की समस्या से परेशान हैं।

🔍 **लक्षण विश्लेषण:**
आपके वर्णित लक्षण आमतौर पर इन कारणों से हो सकते हैं: {', '.join(symptom_info.get('causes', ['सामान्य कारण']))}

💡 **सामान्य सलाह:**
{symptom_info.get('advice', 'आराम करें और पर्याप्त पानी पिएं')}

⚠️ **कब तुरंत डॉक्टर से मिलें:**
{symptom_info.get('emergency', 'यदि लक्षण गंभीर हों या बिगड़ते जाएं')}

📋 **कुछ प्रश्न:**
1. ये लक्षण कब से हैं?
2. कोई अन्य लक्षण भी हैं?
3. क्या आप कोई दवा ले रहे हैं?

**महत्वपूर्ण:** यह केवल सामान्य जानकारी है। कृपया उचित निदान और उपचार के लिए योग्य डॉक्टर से सलाह लें।

क्या आप और कुछ पूछना चाहते हैं?"""

        else:  # English
            return f"""Hello! I'm Dr. Sarvam. I understand you're experiencing {primary_symptom}.

🔍 **Symptom Analysis:**
Your described symptoms could commonly be caused by: {', '.join(symptom_info.get('causes', ['general causes']))}

💡 **General Advice:**
{symptom_info.get('advice', 'Get rest and stay hydrated')}

⚠️ **Seek immediate medical attention if:**
{symptom_info.get('emergency', 'Symptoms are severe or worsening')}

📋 **Follow-up Questions:**
1. How long have you been experiencing these symptoms?
2. Are there any other symptoms?
3. Are you taking any medications?

**Important:** This is general information only. Please consult a qualified healthcare professional for proper diagnosis and treatment.

Is there anything else you'd like to ask?""" 