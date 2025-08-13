"""
RAG (Retrieval-Augmented Generation) System for GP Medical Assistant
Provides accurate medical information by retrieving relevant knowledge
"""

import os
import json
from typing import List, Dict, Optional
from datetime import datetime
import numpy as np

# Vector database and embeddings
try:
    from langchain_community.vectorstores import FAISS, Chroma
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.schema import Document
    from langchain.retrievers import BM25Retriever, EnsembleRetriever
    VECTOR_DB_AVAILABLE = True
except ImportError:
    VECTOR_DB_AVAILABLE = False
    print("⚠️ Vector database dependencies not available. Install with: pip install faiss-cpu chromadb")

class MedicalRAGSystem:
    """RAG system for medical knowledge retrieval"""
    
    def __init__(self, knowledge_base_path: str = "medical_knowledge"):
        self.knowledge_base_path = knowledge_base_path
        self.vector_store = None
        self.retriever = None
        self.embeddings = None
        self.documents = []
        
        # Create knowledge base directory
        os.makedirs(knowledge_base_path, exist_ok=True)
        
        # Initialize embeddings
        self.setup_embeddings()
        
        # Load or create knowledge base
        self.load_medical_knowledge()
        
    def setup_embeddings(self):
        """Setup embedding model"""
        try:
            if VECTOR_DB_AVAILABLE:
                # Use free Hugging Face embeddings
                self.embeddings = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2",
                    model_kwargs={'device': 'cpu'}
                )
                print("✅ Embeddings model loaded")
            else:
                print("⚠️ Using simple keyword matching instead of embeddings")
        except Exception as e:
            print(f"⚠️ Embeddings setup failed: {e}")
            self.embeddings = None
    
    def create_medical_knowledge_base(self):
        """Create comprehensive medical knowledge base"""
        medical_knowledge = [
            # Symptoms and Conditions
            {
                "category": "symptoms",
                "title": "Headache Types and Causes",
                "content": """
                Headaches can be classified into several types:
                
                1. Tension Headaches:
                - Most common type (90% of headaches)
                - Caused by stress, poor posture, eye strain
                - Feels like tight band around head
                - Usually mild to moderate pain
                - Treatment: Rest, hydration, OTC pain relievers
                
                2. Migraine Headaches:
                - Severe throbbing pain, usually one-sided
                - Often accompanied by nausea, light sensitivity
                - Can last 4-72 hours
                - May have aura (visual disturbances)
                - Treatment: Prescription medications, avoid triggers
                
                3. Cluster Headaches:
                - Severe pain around one eye
                - Occurs in clusters over weeks/months
                - More common in men
                - Treatment: Oxygen therapy, prescription medications
                
                4. Sinus Headaches:
                - Pain in forehead, cheeks, around eyes
                - Associated with sinus congestion
                - Often confused with migraines
                - Treatment: Decongestants, treat underlying sinus issue
                
                Red flags requiring immediate medical attention:
                - Sudden severe headache ("worst headache of life")
                - Headache with fever and neck stiffness
                - Headache after head injury
                - Progressive worsening headaches
                - Headache with vision changes or weakness
                """
            },
            {
                "category": "symptoms",
                "title": "Fever Management and Causes",
                "content": """
                Fever is a common symptom indicating the body's immune response:
                
                Normal body temperature: 98.6°F (37°C)
                Fever classifications:
                - Low-grade: 100.4-102°F (38-38.9°C)
                - Moderate: 102-104°F (38.9-40°C)
                - High: Above 104°F (40°C)
                
                Common causes:
                1. Viral infections (most common)
                2. Bacterial infections
                3. Inflammatory conditions
                4. Heat exhaustion
                5. Certain medications
                6. Immunizations
                
                Management:
                - Rest and increased fluid intake
                - Acetaminophen or ibuprofen for comfort
                - Cool compresses
                - Light clothing
                - Monitor temperature regularly
                
                Seek immediate medical care if:
                - Temperature above 103°F (39.4°C)
                - Fever lasting more than 3 days
                - Severe symptoms (difficulty breathing, chest pain)
                - Signs of dehydration
                - Fever in infants under 3 months
                - Fever with severe headache and neck stiffness
                """
            },
            {
                "category": "symptoms",
                "title": "Respiratory Symptoms",
                "content": """
                Common respiratory symptoms and their implications:
                
                1. Cough:
                - Dry cough: Often viral, allergies, or irritants
                - Productive cough: May indicate bacterial infection
                - Chronic cough: Lasting >8 weeks, needs evaluation
                
                2. Sore Throat:
                - Viral (most common): Gradual onset, mild symptoms
                - Bacterial (strep): Sudden onset, severe pain, fever
                - Allergic: Associated with other allergy symptoms
                
                3. Shortness of Breath:
                - Acute: May indicate serious condition
                - Chronic: Could be asthma, COPD, heart disease
                - With chest pain: Possible heart or lung emergency
                
                4. Chest Congestion:
                - Often accompanies upper respiratory infections
                - May progress to lower respiratory tract
                
                Treatment approaches:
                - Viral: Supportive care, rest, fluids
                - Bacterial: May require antibiotics
                - Allergic: Antihistamines, avoid triggers
                
                Seek immediate care for:
                - Severe difficulty breathing
                - Chest pain with shortness of breath
                - High fever with respiratory symptoms
                - Coughing up blood
                - Symptoms worsening rapidly
                """
            },
            {
                "category": "symptoms",
                "title": "Gastrointestinal Issues",
                "content": """
                Common GI symptoms and management:
                
                1. Nausea and Vomiting:
                - Viral gastroenteritis (stomach flu)
                - Food poisoning
                - Motion sickness
                - Medication side effects
                - Pregnancy (morning sickness)
                
                2. Diarrhea:
                - Acute: Usually viral or bacterial
                - Chronic: May indicate underlying condition
                - With blood: Requires medical evaluation
                
                3. Abdominal Pain:
                - Location helps determine cause
                - Upper right: Gallbladder, liver
                - Lower right: Appendix
                - Lower left: Diverticulitis
                - Central: Stomach, small intestine
                
                4. Constipation:
                - Less than 3 bowel movements per week
                - Hard, dry stools
                - Straining during bowel movements
                
                Management:
                - Stay hydrated (especially with vomiting/diarrhea)
                - BRAT diet (bananas, rice, applesauce, toast)
                - Probiotics for digestive health
                - Fiber for constipation
                
                Seek medical care for:
                - Severe abdominal pain
                - Blood in vomit or stool
                - Signs of dehydration
                - Persistent symptoms >48 hours
                - Fever with abdominal pain
                """
            },
            {
                "category": "first_aid",
                "title": "Emergency First Aid",
                "content": """
                Basic first aid for common emergencies:
                
                1. Cuts and Wounds:
                - Apply direct pressure to stop bleeding
                - Clean with water when bleeding stops
                - Apply antibiotic ointment
                - Cover with sterile bandage
                - Seek medical care for deep cuts
                
                2. Burns:
                - Cool with running water for 10-20 minutes
                - Do not use ice
                - Cover with sterile gauze
                - Do not break blisters
                - Seek care for burns larger than palm size
                
                3. Sprains:
                - R.I.C.E. method: Rest, Ice, Compression, Elevation
                - Apply ice for 15-20 minutes every 2-3 hours
                - Use elastic bandage for compression
                - Elevate injured area above heart level
                
                4. Choking:
                - Heimlich maneuver for adults
                - Back blows and chest thrusts for infants
                - Call 911 if object cannot be dislodged
                
                5. Allergic Reactions:
                - Remove or avoid allergen
                - Antihistamines for mild reactions
                - Epinephrine for severe reactions (anaphylaxis)
                - Call 911 for severe reactions
                """
            },
            {
                "category": "prevention",
                "title": "Preventive Health Measures",
                "content": """
                Key preventive health strategies:
                
                1. Vaccination:
                - Annual flu vaccine
                - COVID-19 vaccines and boosters
                - Routine adult vaccines (Tdap, MMR, etc.)
                - Travel vaccines as needed
                
                2. Screening Tests:
                - Blood pressure: Annually
                - Cholesterol: Every 5 years
                - Diabetes: Every 3 years if risk factors
                - Cancer screenings: Age and risk-appropriate
                
                3. Lifestyle Factors:
                - Regular exercise (150 minutes moderate/week)
                - Balanced diet with fruits and vegetables
                - Adequate sleep (7-9 hours/night)
                - Stress management
                - No smoking, limited alcohol
                
                4. Hygiene:
                - Hand washing frequently
                - Dental care (brush twice daily, floss)
                - Safe food handling
                - Clean water consumption
                
                5. Safety:
                - Wear seatbelts and helmets
                - Sun protection (sunscreen, protective clothing)
                - Home safety (smoke detectors, carbon monoxide)
                - Medication safety (proper storage, disposal)
                """
            },
            {
                "category": "medications",
                "title": "Common Over-the-Counter Medications",
                "content": """
                Safe use of common OTC medications:
                
                1. Pain Relievers:
                - Acetaminophen (Tylenol): Safe for most people, max 3000mg/day
                - Ibuprofen (Advil, Motrin): Anti-inflammatory, take with food
                - Aspirin: Blood thinner, avoid in children with viral illness
                
                2. Cold and Allergy:
                - Antihistamines: For allergies, may cause drowsiness
                - Decongestants: For nasal congestion, may raise blood pressure
                - Cough suppressants: For dry cough
                - Expectorants: Help loosen mucus
                
                3. Digestive:
                - Antacids: For heartburn, quick relief
                - H2 blockers: Longer-lasting acid reduction
                - Anti-diarrheal: For temporary diarrhea relief
                - Laxatives: For constipation, use as directed
                
                Important safety tips:
                - Read labels carefully
                - Don't exceed recommended doses
                - Check for drug interactions
                - Consult pharmacist or doctor if unsure
                - Keep medications in original containers
                - Store safely away from children
                """
            }
        ]
        
        # Save knowledge base
        knowledge_file = os.path.join(self.knowledge_base_path, "medical_knowledge.json")
        with open(knowledge_file, 'w', encoding='utf-8') as f:
            json.dump(medical_knowledge, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Created medical knowledge base with {len(medical_knowledge)} entries")
        return medical_knowledge
    
    def load_medical_knowledge(self):
        """Load medical knowledge and create vector store"""
        knowledge_file = os.path.join(self.knowledge_base_path, "medical_knowledge.json")
        
        # Create knowledge base if it doesn't exist
        if not os.path.exists(knowledge_file):
            medical_data = self.create_medical_knowledge_base()
        else:
            with open(knowledge_file, 'r', encoding='utf-8') as f:
                medical_data = json.load(f)
        
        # Convert to documents
        documents = []
        for item in medical_data:
            doc = Document(
                page_content=item['content'],
                metadata={
                    'category': item['category'],
                    'title': item['title'],
                    'source': 'medical_knowledge_base'
                }
            )
            documents.append(doc)
        
        self.documents = documents
        
        # Create vector store if embeddings available
        if VECTOR_DB_AVAILABLE and self.embeddings:
            try:
                # Split documents into chunks
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=500,
                    chunk_overlap=50,
                    separators=["\n\n", "\n", ". ", " "]
                )
                
                split_docs = text_splitter.split_documents(documents)
                
                # Create FAISS vector store
                vector_store_path = os.path.join(self.knowledge_base_path, "vector_store")
                
                if os.path.exists(vector_store_path):
                    # Load existing vector store
                    self.vector_store = FAISS.load_local(
                        vector_store_path, 
                        self.embeddings,
                        allow_dangerous_deserialization=True
                    )
                    print("✅ Loaded existing vector store")
                else:
                    # Create new vector store
                    self.vector_store = FAISS.from_documents(split_docs, self.embeddings)
                    self.vector_store.save_local(vector_store_path)
                    print("✅ Created new vector store")
                
                # Create retriever
                self.retriever = self.vector_store.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": 3}
                )
                
            except Exception as e:
                print(f"⚠️ Vector store creation failed: {e}")
                self.vector_store = None
                self.retriever = None
        
        print(f"✅ Loaded {len(documents)} medical documents")
    
    def retrieve_relevant_info(self, query: str, max_results: int = 3) -> List[Dict]:
        """Retrieve relevant medical information for a query"""
        if self.retriever:
            try:
                # Use vector similarity search
                docs = self.retriever.get_relevant_documents(query)
                
                results = []
                for doc in docs[:max_results]:
                    results.append({
                        'content': doc.page_content,
                        'metadata': doc.metadata,
                        'relevance_score': 0.8  # Placeholder score
                    })
                
                return results
            except Exception as e:
                print(f"⚠️ Vector retrieval failed: {e}")
        
        # Fallback to keyword search
        return self.keyword_search(query, max_results)
    
    def keyword_search(self, query: str, max_results: int = 3) -> List[Dict]:
        """Fallback keyword-based search"""
        query_lower = query.lower()
        results = []
        
        for doc in self.documents:
            content_lower = doc.page_content.lower()
            
            # Simple keyword matching
            matches = 0
            query_words = query_lower.split()
            
            for word in query_words:
                if len(word) > 2:  # Skip very short words
                    matches += content_lower.count(word)
            
            if matches > 0:
                results.append({
                    'content': doc.page_content,
                    'metadata': doc.metadata,
                    'relevance_score': matches / len(query_words),
                    'matches': matches
                })
        
        # Sort by relevance
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return results[:max_results]
    
    def get_context_for_query(self, query: str) -> str:
        """Get relevant context for a medical query"""
        relevant_docs = self.retrieve_relevant_info(query)
        
        if not relevant_docs:
            return "No specific medical information found for this query."
        
        context_parts = []
        for i, doc in enumerate(relevant_docs, 1):
            context_parts.append(f"Medical Reference {i}:")
            context_parts.append(f"Topic: {doc['metadata'].get('title', 'Unknown')}")
            context_parts.append(f"Content: {doc['content'][:500]}...")
            context_parts.append("")
        
        return "\n".join(context_parts)
    
    def add_medical_document(self, title: str, content: str, category: str = "custom"):
        """Add a new medical document to the knowledge base"""
        new_doc = {
            "category": category,
            "title": title,
            "content": content,
            "added_date": datetime.now().isoformat()
        }
        
        # Load existing knowledge
        knowledge_file = os.path.join(self.knowledge_base_path, "medical_knowledge.json")
        if os.path.exists(knowledge_file):
            with open(knowledge_file, 'r', encoding='utf-8') as f:
                medical_data = json.load(f)
        else:
            medical_data = []
        
        # Add new document
        medical_data.append(new_doc)
        
        # Save updated knowledge
        with open(knowledge_file, 'w', encoding='utf-8') as f:
            json.dump(medical_data, f, indent=2, ensure_ascii=False)
        
        # Reload knowledge base
        self.load_medical_knowledge()
        
        print(f"✅ Added new medical document: {title}")
    
    def get_statistics(self) -> Dict:
        """Get RAG system statistics"""
        return {
            'total_documents': len(self.documents),
            'vector_store_available': self.vector_store is not None,
            'embeddings_available': self.embeddings is not None,
            'knowledge_base_path': self.knowledge_base_path,
            'categories': list(set(doc.metadata.get('category', 'unknown') for doc in self.documents))
        }

# Global RAG instance
rag_system = None

def initialize_rag():
    """Initialize the RAG system"""
    global rag_system
    if rag_system is None:
        rag_system = MedicalRAGSystem()
    return rag_system

def get_medical_context(query: str) -> str:
    """Get medical context for a query"""
    if rag_system is None:
        initialize_rag()
    
    return rag_system.get_context_for_query(query)

def add_medical_knowledge(title: str, content: str, category: str = "custom"):
    """Add new medical knowledge"""
    if rag_system is None:
        initialize_rag()
    
    rag_system.add_medical_document(title, content, category)

if __name__ == "__main__":
    # Test the RAG system
    print("🧠 Testing Medical RAG System")
    print("=" * 40)
    
    rag = MedicalRAGSystem()
    
    # Test queries
    test_queries = [
        "I have a severe headache",
        "What should I do for a fever?",
        "I'm coughing and have a sore throat",
        "How to treat a cut?"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        context = rag.get_context_for_query(query)
        print(f"📚 Context: {context[:200]}...")
    
    # Show statistics
    stats = rag.get_statistics()
    print(f"\n📊 RAG Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")