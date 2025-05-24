#!/usr/bin/env python3
"""
Setup script for Multilingual AI Doctor Agent
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"📋 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def create_env_file():
    """Create .env file from template"""
    env_path = Path('.env')
    template_path = Path('env_example.txt')
    
    if env_path.exists():
        print("⚠️  .env file already exists, skipping creation")
        return True
    
    if template_path.exists():
        with open(template_path, 'r') as template:
            content = template.read()
        
        with open(env_path, 'w') as env_file:
            env_file.write(content)
        
        print("✅ .env file created from template")
        print("📝 Please edit .env file and add your Sarvam AI API key")
        return True
    else:
        print("❌ env_example.txt not found")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['static/css', 'static/js', 'templates', 'logs']
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Created necessary directories")
    return True

def install_dependencies():
    """Install Python dependencies"""
    return run_command("pip install -r requirements.txt", "Installing Python dependencies")

def check_sarvam_api():
    """Check if Sarvam AI API key is configured"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('SARVAM_API_KEY')
        if api_key and api_key != 'your_sarvam_ai_api_key_here':
            print("✅ Sarvam AI API key configured")
            return True
        else:
            print("⚠️  Sarvam AI API key not configured")
            print("📝 Please edit .env file and add your API key")
            return False
    except ImportError:
        print("⚠️  python-dotenv not installed, cannot check API key")
        return False

def main():
    """Main setup function"""
    print("🏥 Setting up Multilingual AI Doctor Agent")
    print("=" * 50)
    
    steps = [
        ("Checking Python version", check_python_version),
        ("Creating directories", create_directories),
        ("Installing dependencies", install_dependencies),
        ("Creating .env file", create_env_file),
        ("Checking Sarvam AI configuration", check_sarvam_api),
    ]
    
    success_count = 0
    for description, function in steps:
        if function():
            success_count += 1
        print()
    
    print("=" * 50)
    print(f"Setup completed: {success_count}/{len(steps)} steps successful")
    
    if success_count == len(steps):
        print("🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Make sure your Sarvam AI API key is set in .env file")
        print("2. Run: python app.py")
        print("3. Open: http://localhost:5000")
    else:
        print("⚠️  Setup completed with some issues")
        print("Please check the errors above and fix them before running the application")
    
    print("\n📖 For more information, see README.md")

if __name__ == "__main__":
    main() 