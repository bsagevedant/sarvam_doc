#!/usr/bin/env python3
"""
Demo script for Multilingual AI Doctor Agent
Demonstrates core functionality without web interface
"""

import os
from medical_ai import MedicalAI
from config import Config

def print_banner():
    """Print application banner"""
    print("🏥" + "=" * 60 + "🏥")
    print("    Dr. Sarvam - Multilingual AI Doctor Agent Demo")
    print("🏥" + "=" * 60 + "🏥")
    print()

def demo_language_support():
    """Demonstrate language support"""
    print("🌐 SUPPORTED LANGUAGES:")
    print("-" * 40)
    for code, name in Config.LANGUAGE_NAMES.items():
        print(f"  {code}: {name}")
    print()

def demo_medical_ai():
    """Demonstrate medical AI capabilities"""
    print("🤖 MEDICAL AI DEMONSTRATION:")
    print("-" * 40)
    
    medical_ai = MedicalAI()
    
    # Test cases in different languages
    test_cases = [
        {
            "query": "I have a high fever and headache",
            "language": "en",
            "description": "English symptom query"
        },
        {
            "query": "मुझे सिरदर्द हो रहा है और बुखार है",
            "language": "hi", 
            "description": "Hindi symptom query"
        },
        {
            "query": "I have severe chest pain",
            "language": "en",
            "description": "Emergency case"
        },
        {
            "query": "How can I stay healthy?",
            "language": "en",
            "description": "General health query"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: {case['description']}")
        print(f"   Query: {case['query']}")
        print(f"   Language: {Config.LANGUAGE_NAMES.get(case['language'], case['language'])}")
        
        # Detect symptoms
        symptoms = medical_ai.detect_symptoms(case['query'])
        print(f"   Detected Symptoms: {symptoms if symptoms else 'None'}")
        
        # Check emergency
        is_emergency = medical_ai.check_emergency(case['query'])
        print(f"   Emergency Detected: {'🚨 YES' if is_emergency else '✅ No'}")
        
        # Generate response
        response = medical_ai.generate_medical_response(case['query'], case['language'])
        print(f"   Response Preview: {response[:100]}...")
        print()

def demo_symptom_detection():
    """Demonstrate symptom detection patterns"""
    print("🔍 SYMPTOM DETECTION DEMONSTRATION:")
    print("-" * 40)
    
    medical_ai = MedicalAI()
    
    test_symptoms = [
        "I have fever",
        "मुझे बुखार है",
        "headache problem",
        "सिर में दर्द",
        "coughing a lot",
        "खांसी आ रही है",
        "stomach pain",
        "पेट में दर्द",
        "runny nose",
        "नाक बह रही है"
    ]
    
    for symptom_text in test_symptoms:
        symptoms = medical_ai.detect_symptoms(symptom_text)
        print(f"  '{symptom_text}' → {symptoms}")
    print()

def demo_emergency_detection():
    """Demonstrate emergency detection"""
    print("🚨 EMERGENCY DETECTION DEMONSTRATION:")
    print("-" * 40)
    
    medical_ai = MedicalAI()
    
    emergency_cases = [
        "I have severe chest pain",
        "सीने में तेज दर्द है",
        "difficulty breathing",
        "सांस लेने में तकलीफ",
        "heart attack symptoms",
        "हार्ट अटैक के लक्षण",
        "unconscious patient",
        "बेहोशी की हालत"
    ]
    
    non_emergency_cases = [
        "mild headache",
        "हल्का सिरदर्द",
        "common cold",
        "सामान्य जुकाम"
    ]
    
    print("  Emergency Cases:")
    for case in emergency_cases:
        is_emergency = medical_ai.check_emergency(case)
        status = "🚨 EMERGENCY" if is_emergency else "❌ NOT DETECTED"
        print(f"    '{case}' → {status}")
    
    print("\n  Non-Emergency Cases:")
    for case in non_emergency_cases:
        is_emergency = medical_ai.check_emergency(case)
        status = "🚨 FALSE POSITIVE" if is_emergency else "✅ CORRECT"
        print(f"    '{case}' → {status}")
    print()

def demo_interactive_consultation():
    """Interactive consultation demo"""
    print("💬 INTERACTIVE CONSULTATION DEMO:")
    print("-" * 40)
    print("Enter your health concerns (type 'quit' to exit)")
    print("You can type in English or Hindi")
    print()
    
    medical_ai = MedicalAI()
    
    while True:
        try:
            query = input("Patient: ").strip()
            
            if query.lower() in ['quit', 'exit', 'bye', 'quit()']:
                print("Dr. Sarvam: Thank you for using Dr. Sarvam. Take care! 🏥")
                break
            
            if not query:
                continue
            
            # Detect language (simplified)
            language = 'hi' if any(ord(char) > 127 for char in query) else 'en'
            
            # Generate response
            response = medical_ai.generate_medical_response(query, language)
            print(f"\nDr. Sarvam: {response}\n")
            print("-" * 60)
            
        except KeyboardInterrupt:
            print("\n\nDr. Sarvam: Consultation ended. Take care! 🏥")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Main demo function"""
    print_banner()
    
    while True:
        print("📋 DEMO OPTIONS:")
        print("1. Language Support")
        print("2. Medical AI Capabilities")
        print("3. Symptom Detection")
        print("4. Emergency Detection")
        print("5. Interactive Consultation")
        print("6. Exit")
        print()
        
        try:
            choice = input("Select an option (1-6): ").strip()
            print()
            
            if choice == '1':
                demo_language_support()
            elif choice == '2':
                demo_medical_ai()
            elif choice == '3':
                demo_symptom_detection()
            elif choice == '4':
                demo_emergency_detection()
            elif choice == '5':
                demo_interactive_consultation()
            elif choice == '6':
                print("Thank you for using Dr. Sarvam Demo! 🏥")
                break
            else:
                print("Invalid option. Please select 1-6.")
            
            if choice != '5':
                input("Press Enter to continue...")
                print("\n" + "="*60 + "\n")
                
        except KeyboardInterrupt:
            print("\n\nDemo ended. Goodbye! 🏥")
            break

if __name__ == "__main__":
    main() 