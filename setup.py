#!/usr/bin/env python3
"""
Setup script for GP Medical Assistant Chatbot
"""

import os
import subprocess
import sys

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False

def setup_environment():
    """Setup environment file"""
    if not os.path.exists('.env'):
        print("📝 Creating environment file...")
        with open('.env.example', 'r') as example:
            content = example.read()
        
        with open('.env', 'w') as env_file:
            env_file.write(content)
        
        print("✅ Environment file created!")
        print("🔑 Please edit .env and add your Google Gemini API key")
        print("🔗 Get your API key from: https://makersuite.google.com/app/apikey")
        return False
    else:
        print("✅ Environment file already exists")
        return True

def create_logs_directory():
    """Create logs directory"""
    os.makedirs("logs", exist_ok=True)
    print("✅ Logs directory created")

def main():
    """Main setup function"""
    print("🩺 GP Medical Assistant Setup")
    print("=" * 40)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Setup environment
    env_ready = setup_environment()
    
    # Create logs directory
    create_logs_directory()
    
    print("\n🎉 Setup completed!")
    
    if not env_ready:
        print("\n⚠️  Next steps:")
        print("1. Edit .env file and add your Google Gemini API key")
        print("2. Run: python run.py")
    else:
        print("\n🚀 You can now run: python run.py")

if __name__ == '__main__':
    main()