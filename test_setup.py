#!/usr/bin/env python3
"""
Test script for Multilingual AI Doctor Agent
"""

import sys
import os
import requests
import time
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import flask
        print("✅ Flask imported successfully")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        from config import Config
        print("✅ Config imported successfully")
    except ImportError as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from sarvam_client import SarvamAIClient
        print("✅ SarvamAIClient imported successfully")
    except ImportError as e:
        print(f"❌ SarvamAIClient import failed: {e}")
        return False
    
    try:
        from medical_ai import MedicalAI
        print("✅ MedicalAI imported successfully")
    except ImportError as e:
        print(f"❌ MedicalAI import failed: {e}")
        return False
    
    return True

def test_config():
    """Test configuration settings"""
    print("\n🧪 Testing configuration...")
    
    try:
        from config import Config
        
        # Check if required configs exist
        if hasattr(Config, 'SUPPORTED_LANGUAGES'):
            print(f"✅ Supported languages: {len(Config.SUPPORTED_LANGUAGES)} languages")
        else:
            print("❌ SUPPORTED_LANGUAGES not found in config")
            return False
        
        if hasattr(Config, 'LANGUAGE_NAMES'):
            print(f"✅ Language names: {len(Config.LANGUAGE_NAMES)} entries")
        else:
            print("❌ LANGUAGE_NAMES not found in config")
            return False
        
        print(f"✅ API Key configured: {'Yes' if Config.SARVAM_API_KEY else 'No'}")
        
        return True
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def test_medical_ai():
    """Test medical AI functionality"""
    print("\n🧪 Testing Medical AI...")
    
    try:
        from medical_ai import MedicalAI
        
        medical_ai = MedicalAI()
        
        # Test symptom detection
        test_queries = [
            "I have a fever",
            "मुझे सिरदर्द हो रहा है",
            "I have chest pain"  # Should trigger emergency
        ]
        
        for query in test_queries:
            symptoms = medical_ai.detect_symptoms(query)
            emergency = medical_ai.check_emergency(query)
            response = medical_ai.generate_medical_response(query, 'en')
            
            print(f"✅ Query '{query}' processed successfully")
            print(f"   Symptoms: {symptoms}")
            print(f"   Emergency: {emergency}")
            print(f"   Response length: {len(response)} chars")
        
        return True
    except Exception as e:
        print(f"❌ Medical AI test failed: {e}")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("\n🧪 Testing file structure...")
    
    required_files = [
        'app.py',
        'config.py',
        'sarvam_client.py',
        'medical_ai.py',
        'requirements.txt',
        'templates/index.html',
        'static/css/style.css',
        'static/js/app.js'
    ]
    
    missing_files = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def test_app_startup():
    """Test if the Flask app can start (without running it)"""
    print("\n🧪 Testing app startup...")
    
    try:
        from app import app
        
        # Test app configuration
        print(f"✅ Flask app created successfully")
        print(f"✅ Debug mode: {app.debug}")
        
        # Test route registration
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        print(f"✅ Routes registered: {len(routes)}")
        
        required_routes = ['/', '/api/health', '/api/consult', '/api/audio-consult']
        missing_routes = [route for route in required_routes if route not in routes]
        
        if missing_routes:
            print(f"❌ Missing routes: {missing_routes}")
            return False
        else:
            print("✅ All required routes registered")
        
        return True
    except Exception as e:
        print(f"❌ App startup test failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🏥 Testing Multilingual AI Doctor Agent")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Medical AI", test_medical_ai),
        ("App Startup", test_app_startup),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} test...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} test PASSED")
            else:
                print(f"❌ {test_name} test FAILED")
        except Exception as e:
            print(f"❌ {test_name} test ERROR: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to run.")
        print("\n📋 To start the application:")
        print("1. python app.py")
        print("2. Open http://localhost:5000")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 