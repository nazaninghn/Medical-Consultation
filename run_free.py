#!/usr/bin/env python3
"""
GP Medical Assistant with Free Models
Run with Hugging Face, Ollama, or other free AI models
"""

import os
import sys
from dotenv import load_dotenv

def setup_free_models():
    """Setup free models environment"""
    print("🤗 GP Medical Assistant - Free Models Edition")
    print("=" * 50)
    
    # Load free models environment
    if os.path.exists('.env.free'):
        load_dotenv('.env.free')
        print("✅ Loaded free models configuration")
    else:
        print("⚠️  No .env.free found, using defaults")
    
    # Get model configuration
    provider = os.getenv('MODEL_PROVIDER', 'huggingface')
    model_name = os.getenv('MODEL_NAME', 'medical_zephyr')
    
    print(f"🔧 Model Provider: {provider}")
    print(f"🤖 Model Name: {model_name}")
    
    return provider, model_name

def check_dependencies(provider):
    """Check if required dependencies are installed"""
    missing_deps = []
    
    try:
        import flask
        import langchain
    except ImportError as e:
        missing_deps.append("Basic dependencies")
    
    if provider == 'huggingface':
        try:
            import transformers
            import torch
        except ImportError:
            missing_deps.append("transformers torch")
    
    elif provider == 'ollama':
        # Ollama doesn't need extra Python packages, just the Ollama server
        print("📝 Note: Make sure Ollama is installed and running")
        print("   Install: https://ollama.ai/download")
        print("   Run: ollama pull llama2")
    
    if missing_deps:
        print("❌ Missing dependencies:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\n📦 Install with: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main function to start the free models application"""
    provider, model_name = setup_free_models()
    
    if not check_dependencies(provider):
        print("\n🔧 Please install missing dependencies first")
        sys.exit(1)
    
    print("✅ All dependencies satisfied")
    print("🚀 Starting the medical assistant with free models...")
    print(f"\n📱 Open your browser and go to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Import and run the free models application
    try:
        from main_free import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Medical assistant stopped. Stay healthy!")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("\n🔄 Falling back to simple mode...")
        
        # Try fallback
        try:
            os.environ['MODEL_PROVIDER'] = 'simple'
            from main_free import app
            app.run(debug=True, host='0.0.0.0', port=5000)
        except Exception as fallback_error:
            print(f"❌ Fallback also failed: {fallback_error}")
            sys.exit(1)

if __name__ == '__main__':
    main()