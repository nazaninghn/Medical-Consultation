#!/usr/bin/env python3
"""
Test script to demonstrate RAG database retrieval
"""

from rag_system import initialize_rag, get_medical_context

def test_rag_retrieval():
    """Test RAG database retrieval with sample queries"""
    print("🧠 Testing RAG Database Retrieval")
    print("=" * 40)
    
    # Initialize RAG system
    print("🔄 Initializing RAG system...")
    rag = initialize_rag()
    
    # Test queries
    test_queries = [
        "I have a severe headache with nausea",
        "What should I do for a high fever?",
        "I'm coughing and have a sore throat",
        "How to treat a cut on my hand?",
        "What medications can I take for pain?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}: {query}")
        print("-" * 30)
        
        # Get medical context from RAG
        context = get_medical_context(query)
        
        if context and "No specific medical information found" not in context:
            print("✅ RAG Retrieved Relevant Information:")
            print(context[:300] + "..." if len(context) > 300 else context)
        else:
            print("❌ No relevant information found")
    
    # Show RAG statistics
    stats = rag.get_statistics()
    print(f"\n📊 RAG System Statistics:")
    print(f"   Documents: {stats['total_documents']}")
    print(f"   Categories: {', '.join(stats['categories'])}")
    print(f"   Vector Store: {'Available' if stats['vector_store_available'] else 'Unavailable'}")
    print(f"   Embeddings: {'Available' if stats['embeddings_available'] else 'Unavailable'}")

if __name__ == "__main__":
    test_rag_retrieval()