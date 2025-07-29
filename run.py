#!/usr/bin/env python3
"""
GP Medical Assistant Chatbot
A Flask-based web application for medical symptom consultation
"""

import os
import sys
from dotenv import load_dotenv

def check_requirements():
    """Check if all required packages are installed"""
    # Map package names to their import names
    required_packages = {
        'flask': 'flask',
        'flask-cors': 'flask_cors',
        'langchain': 'langchain',
        'langchain-google-genai': 'langchain_google_genai',
        'pydantic': 'pydantic',
        'python-dotenv': 'dotenv'
    }
    
    missing_packages = []
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install missing packages with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_env_file():
    """Check if environment file exists and has required variables"""
    env_path = '.env'
    if not os.path.exists(env_path):
        print("❌ Environment file not found at .env")
        print("📝 Please create .env with your Google API key:")
        print("   GOOGLE_API_KEY=your_actual_api_key_here")
        return False
    
    load_dotenv(env_path)
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key or api_key == 'your_google_gemini_api_key_here':
        print("❌ Google API key not configured")
        print("📝 Please update .env with your actual Google Gemini API key:")
        print("   GOOGLE_API_KEY=your_actual_api_key_here")
        print("\n🔗 Get your API key from: https://makersuite.google.com/app/apikey")
        return False
    
    return True

def main():
    """Main function to start the application"""
    print("🩺 GP Medical Assistant Chatbot")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment
    if not check_env_file():
        sys.exit(1)
    
    print("✅ All requirements satisfied")
    print("🚀 Starting the medical assistant...")
    print("\n📱 Open your browser and go to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 40)
    
    # Import and run the main application
    try:
        from main import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Medical assistant stopped. Stay healthy!")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()