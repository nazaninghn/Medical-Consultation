# 📍 **AI Model Components Location Map**

## 🗂️ **Project Structure Overview**

```
📁 GP-Medical-Assistant/
├── 🤖 AI Models Configuration
├── 🧠 RAG System Components  
├── 🌐 Web Application Files
├── 🚀 Deployment Configurations
└── 📚 Documentation & Guides
```

---

## 🤗 **Hugging Face Models (Free Options)**

### **⭐⭐⭐⭐⭐ Zephyr-7B: `HuggingFaceH4/zephyr-7b-beta`**

#### **📁 Configuration:**
- **File**: `models_config.py` (Lines 28-33)
- **Key**: `medical_zephyr`
- **Model ID**: `HuggingFaceH4/zephyr-7b-beta`

#### **🔧 Implementation:**
- **File**: `main_free.py` (Lines 33-49)
- **Function**: `create_huggingface_llm()`
- **Library**: `langchain_huggingface.HuggingFacePipeline`

#### **🚀 Runner:**
- **File**: `run_free.py`
- **Environment**: `MODEL_PROVIDER=huggingface`, `MODEL_NAME=medical_zephyr`

---

### **⭐⭐⭐⭐ Mistral-7B: `mistralai/Mistral-7B-Instruct-v0.1`**

#### **📁 Configuration:**
- **File**: `models_config.py` (Lines 16-21)
- **Key**: `medical_mistral`
- **Model ID**: `mistralai/Mistral-7B-Instruct-v0.1`

#### **🔧 Implementation:**
- **File**: `main_free.py` (Lines 33-49)
- **Function**: `create_huggingface_llm()`
- **Library**: `transformers.pipeline`

#### **🚀 Usage:**
```bash
# Set in .env file
MODEL_PROVIDER=huggingface
MODEL_NAME=medical_mistral
```

---

### **⭐⭐⭐⭐ Llama2-7B: `meta-llama/Llama-2-7b-chat-hf`**

#### **📁 Configuration:**
- **File**: `models_config.py` (Lines 22-27)
- **Key**: `medical_llama2`
- **Model ID**: `meta-llama/Llama-2-7b-chat-hf`

#### **🔧 Implementation:**
- **File**: `main_free.py` (Lines 33-49)
- **Function**: `create_huggingface_llm()`
- **Requirements**: `transformers>=4.35.0`, `torch>=2.0.0`

#### **🚀 Usage:**
```bash
# Set in .env file
MODEL_PROVIDER=huggingface
MODEL_NAME=medical_llama2
```

---

### **⭐⭐⭐⭐ OpenChat-3.5: `openchat/openchat-3.5-1210`**

#### **📁 Configuration:**
- **File**: `models_config.py` (Lines 34-39)
- **Key**: `medical_openchat`
- **Model ID**: `openchat/openchat-3.5-1210`

#### **🔧 Implementation:**
- **File**: `main_free.py` (Lines 33-49)
- **Function**: `create_huggingface_llm()`
- **Pipeline**: `text-generation`

#### **🚀 Usage:**
```bash
# Set in .env file
MODEL_PROVIDER=huggingface
MODEL_NAME=medical_openchat
```

---

## 🦙 **Ollama Local Models (Privacy-Focused)**

### **Llama 2: `llama2:7b`**

#### **📁 Configuration:**
- **File**: `models_config.py` (Lines 44-48)
- **Key**: `llama2`
- **Model Name**: `llama2:7b`

#### **🔧 Implementation:**
- **File**: `main_free.py` (Lines 55-67)
- **Function**: `create_ollama_llm()`
- **Library**: `langchain_community.llms.Ollama`

#### **🚀 Setup:**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull model
ollama pull llama2:7b

# Configure
MODEL_PROVIDER=ollama
MODEL_NAME=llama2
```

---

### **Mistral: `mistral:7b`**

#### **📁 Configuration:**
- **File**: `models_config.py` (Lines 49-53)
- **Key**: `mistral`
- **Model Name**: `mistral:7b`

#### **🔧 Implementation:**
- **File**: `main_free.py` (Lines 55-67)
- **Function**: `create_ollama_llm()`
- **Connection**: Local Ollama server

#### **🚀 Setup:**
```bash
# Pull Mistral model
ollama pull mistral:7b

# Configure
MODEL_PROVIDER=ollama
MODEL_NAME=mistral
```

---

### **Medical Llama: `medllama2:7b`**

#### **📁 Configuration:**
- **File**: `models_config.py` (Lines 59-63)
- **Key**: `medllama`
- **Model Name**: `medllama2:7b`

#### **🔧 Implementation:**
- **File**: `main_free.py` (Lines 55-67)
- **Function**: `create_ollama_llm()`
- **Specialty**: Medical-focused responses

#### **🚀 Setup:**
```bash
# Pull Medical Llama model
ollama pull medllama2:7b

# Configure
MODEL_PROVIDER=ollama
MODEL_NAME=medllama
```

---

### **Code Llama: `codellama:7b`**

#### **📁 Configuration:**
- **File**: `models_config.py` (Lines 54-58)
- **Key**: `codellama`
- **Model Name**: `codellama:7b`

#### **🔧 Implementation:**
- **File**: `main_free.py` (Lines 55-67)
- **Function**: `create_ollama_llm()`
- **Specialty**: Technical understanding

#### **🚀 Setup:**
```bash
# Pull Code Llama model
ollama pull codellama:7b

# Configure
MODEL_PROVIDER=ollama
MODEL_NAME=codellama
```

---

## 🌐 **Free API Services**

### **Configuration Location:**
- **File**: `models_config.py` (Lines 66-85)
- **Services**: Together AI, Groq, Perplexity

### **Implementation Location:**
- **File**: `main_free.py` (Lines 69-83)
- **Function**: `create_free_api_llm()`
- **Library**: `langchain_openai.ChatOpenAI`

---

## 🧠 **RAG System Components**

### **Main RAG System:**
- **File**: `rag_system.py`
- **Class**: `MedicalRAGSystem`
- **Database**: `medical_knowledge/`

### **Vector Database:**
- **Location**: `medical_knowledge/vector_store/`
- **Files**: `index.faiss`, `index.pkl`
- **Library**: FAISS (Facebook AI Similarity Search)

### **Knowledge Base:**
- **Location**: `medical_knowledge/medical_knowledge.json`
- **Content**: 7 medical documents
- **Categories**: Symptoms, First Aid, Prevention, Medications

### **Embeddings:**
- **Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Implementation**: `rag_system.py` (Lines 45-55)
- **Library**: `sentence_transformers`

---

## 🌐 **Web Application Components**

### **Main Applications:**
- **Standard**: `main.py` (Google Gemini)
- **Free Models**: `main_free.py` (Hugging Face, Ollama)
- **RAG Enhanced**: `main_rag.py` (RAG + Any model)

### **Frontend:**
- **Location**: `templates/index.html`
- **Features**: Responsive UI, Voice I/O, File Upload
- **Styling**: Embedded CSS with luxury design

### **Runners:**
- **Standard**: `run.py`
- **Free Models**: `run_free.py`
- **RAG Enhanced**: `run_rag.py`

---

## 🔧 **Configuration Files**

### **Environment Configuration:**
- **Main**: `.env`
- **Free Models**: `.env.free`
- **Example**: `.env.example`

### **Model Selection:**
```bash
# Hugging Face Models
MODEL_PROVIDER=huggingface
MODEL_NAME=medical_zephyr    # or medical_mistral, medical_llama2, medical_openchat

# Ollama Models  
MODEL_PROVIDER=ollama
MODEL_NAME=llama2           # or mistral, codellama, medllama

# Free API Services
MODEL_PROVIDER=free_api
MODEL_NAME=together        # or groq, perplexity
```

---

## 🚀 **Deployment Components**

### **Cloud Deployment:**
- **Render**: `render.yaml`
- **Railway**: `railway.json`
- **Vercel**: `vercel.json`
- **Docker**: `Dockerfile`

### **API Structure:**
- **Vercel**: `api/index.py`
- **Requirements**: `api/requirements.txt`

---

## 📚 **Documentation & Management**

### **Guides:**
- **Free Models**: `FREE_MODELS_GUIDE.md`
- **RAG System**: `RAG_GUIDE.md`
- **Deployment**: `DEPLOY_OPTIONS.md`

### **Management Tools:**
- **RAG Database**: `rag_database_manager.py`
- **RAG Testing**: `test_rag_database.py`
- **API Testing**: `test_api.py`

---

## 🔍 **How to Use Each Component**

### **🤗 Hugging Face Models:**
```bash
# 1. Configure
echo "MODEL_PROVIDER=huggingface" > .env
echo "MODEL_NAME=medical_zephyr" >> .env

# 2. Install dependencies
pip install transformers torch langchain-huggingface

# 3. Run
python run_free.py
```

### **🦙 Ollama Models:**
```bash
# 1. Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Pull model
ollama pull llama2:7b

# 3. Configure
echo "MODEL_PROVIDER=ollama" > .env
echo "MODEL_NAME=llama2" >> .env

# 4. Run
python run_free.py
```

### **🧠 RAG Enhanced:**
```bash
# 1. Install RAG dependencies
pip install faiss-cpu sentence-transformers

# 2. Enable RAG
echo "USE_RAG=true" >> .env

# 3. Run
python run_rag.py
```

---

## 📊 **Component Dependencies**

### **Hugging Face Models:**
```python
transformers>=4.35.0
torch>=2.0.0
langchain-huggingface>=0.0.1
huggingface-hub>=0.17.0
```

### **Ollama Models:**
```python
langchain-community>=0.0.10
# + Ollama server installation
```

### **RAG System:**
```python
faiss-cpu>=1.7.4
sentence-transformers>=2.2.0
chromadb>=0.4.0  # Alternative
numpy>=1.24.0
```

### **Web Application:**
```python
flask>=3.0.0
flask-cors>=4.0.0
gunicorn>=21.2.0  # Production
```

---

## 🎯 **Quick Access Commands**

### **View All Models:**
```bash
python -c "from models_config import get_available_models; import json; print(json.dumps(get_available_models(), indent=2))"
```

### **Test Specific Model:**
```bash
# Hugging Face
MODEL_PROVIDER=huggingface MODEL_NAME=medical_zephyr python run_free.py

# Ollama
MODEL_PROVIDER=ollama MODEL_NAME=llama2 python run_free.py

# RAG Enhanced
USE_RAG=true python run_rag.py
```

### **Check RAG Database:**
```bash
python rag_database_manager.py
```

---

**🎉 All components are organized, documented, and ready to use! Each model type has its specific location, configuration, and implementation details clearly mapped out.**