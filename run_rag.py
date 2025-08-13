#!/usr/bin/env python3
"""
GP Medical Assistant with RAG (Retrieval-Augmented Generation)
Enhanced with medical knowledge base for accurate responses
"""

import os
import sys
from dotenv import load_dotenv

def setup_rag_environment():
    """Setup RAG environment"""
    print("🧠 GP Medical Assistant - RAG Enhanced Edition")
    print("=" * 55)
    
    # Load environment variables
    load_dotenv()
    
    # RAG configuration
    use_rag = os.getenv('USE_RAG', 'true').lower() == 'true'
    model_provider = os.getenv('MODEL_PROVIDER', 'simple')
    
    print(f"📚 RAG System: {'Enabled' if use_rag else 'Disabled'}")
    print(f"🤖 Model Provider: {model_provider}")
    
    return use_rag, model_provider

def check_rag_dependencies():
    """Check if RAG dependencies are installed"""
    missing_deps = []
    
    # Basic dependencies
    try:
        import flask
        import langchain
        import numpy
    except ImportError:
        missing_deps.append("Basic dependencies (flask, langchain, numpy)")
    
    # RAG-specific dependencies
    try:
        import faiss
    except ImportError:
        missing_deps.append("faiss-cpu (vector database)")
    
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        missing_deps.append("sentence-transformers (embeddings)")
    
    try:
        import chromadb
    except ImportError:
        missing_deps.append("chromadb (alternative vector database)")
    
    if missing_deps:
        print("❌ Missing RAG dependencies:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\n📦 Install with: pip install -r requirements.txt")
        print("💡 Or install minimal RAG: pip install faiss-cpu sentence-transformers")
        return False
    
    return True

def initialize_rag_system():
    """Initialize the RAG system"""
    try:
        print("🔄 Initializing RAG system...")
        from rag_system import initialize_rag
        
        rag = initialize_rag()
        stats = rag.get_statistics()
        
        print("✅ RAG system initialized successfully!")
        print(f"📊 Knowledge base: {stats['total_documents']} documents")
        print(f"🏷️  Categories: {', '.join(stats['categories'])}")
        print(f"🔍 Vector search: {'Available' if stats['vector_store_available'] else 'Fallback to keyword search'}")
        
        return True
        
    except Exception as e:
        print(f"⚠️ RAG initialization failed: {e}")
        print("🔄 Will use simple keyword-based responses")
        return False

def main():
    """Main function to start the RAG-enhanced application"""
    use_rag, model_provider = setup_rag_environment()
    
    # Check dependencies
    if use_rag:
        if not check_rag_dependencies():
            print("\n🔧 RAG dependencies missing. Options:")
            print("1. Install dependencies: pip install -r requirements.txt")
            print("2. Disable RAG: Set USE_RAG=false in .env")
            print("3. Continue with simple responses (y/n)?")
            
            choice = input().lower()
            if choice != 'y':
                sys.exit(1)
            else:
                os.environ['USE_RAG'] = 'false'
                use_rag = False
    
    # Initialize RAG if enabled
    if use_rag:
        rag_ready = initialize_rag_system()
        if not rag_ready:
            print("⚠️ Continuing without RAG enhancement")
    
    print("✅ All systems ready")
    print("🚀 Starting the RAG-enhanced medical assistant...")
    print(f"\n📱 Open your browser and go to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 55)
    
    # Import and run the RAG application
    try:
        from main_rag import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 RAG-enhanced medical assistant stopped. Stay healthy!")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("\n🔄 Trying fallback mode...")
        
        # Try fallback
        try:
            os.environ['USE_RAG'] = 'false'
            from main_rag import app
            app.run(debug=True, host='0.0.0.0', port=5000)
        except Exception as fallback_error:
            print(f"❌ Fallback also failed: {fallback_error}")
            sys.exit(1)

if __name__ == '__main__':
    main()