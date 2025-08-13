# 🤗 Free AI Models for GP Medical Assistant

## 🎯 **Why Use Free Models?**

- ✅ **No API costs** - Completely free to use
- ✅ **Privacy** - Your data stays local/private
- ✅ **No rate limits** - Use as much as you want
- ✅ **Offline capable** - Some models work without internet
- ✅ **Open source** - Transparent and customizable

## 🚀 **Quick Start with Free Models**

### **Option 1: Hugging Face Models (Recommended)**

```bash
# 1. Copy free models environment
cp .env.free .env

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run with free models
python run_free.py
```

### **Option 2: Local Ollama Models**

```bash
# 1. Install Ollama
# Visit: https://ollama.ai/download

# 2. Pull a model
ollama pull llama2:7b

# 3. Configure environment
echo "MODEL_PROVIDER=ollama" > .env
echo "MODEL_NAME=llama2" >> .env

# 4. Run
python run_free.py
```

## 🤖 **Available Free Models**

### **🤗 Hugging Face Models**

| Model | Description | Size | Quality |
|-------|-------------|------|---------|
| **Zephyr-7B** | High-quality instruction model | 7B | ⭐⭐⭐⭐⭐ |
| **Mistral-7B** | Fast and efficient | 7B | ⭐⭐⭐⭐ |
| **Llama2-7B** | Meta's popular model | 7B | ⭐⭐⭐⭐ |
| **OpenChat-3.5** | Conversation optimized | 7B | ⭐⭐⭐⭐ |

### **🦙 Ollama Local Models**

| Model | Command | Description |
|-------|---------|-------------|
| **Llama 2** | `ollama pull llama2:7b` | General purpose |
| **Mistral** | `ollama pull mistral:7b` | Fast inference |
| **Code Llama** | `ollama pull codellama:7b` | Code understanding |
| **Med Llama** | `ollama pull medllama2:7b` | Medical focused |

### **🌐 Free API Services**

| Service | Free Tier | Models Available |
|---------|-----------|------------------|
| **Together AI** | $25 credit | Llama 2, Mistral, etc. |
| **Groq** | Free tier | Llama 2, Mixtral |
| **Perplexity** | Limited free | Various models |

## ⚙️ **Configuration Options**

### **Environment Variables (.env)**

```bash
# Model Provider
MODEL_PROVIDER=huggingface  # huggingface, ollama, free_api

# Model Selection
MODEL_NAME=medical_zephyr   # Depends on provider

# Performance Options
USE_GPU=false              # Use GPU for Hugging Face models
HUGGINGFACE_TOKEN=         # Optional: For private models
FREE_API_KEY=              # Required for free API services
```

### **Model Provider Details**

#### **Hugging Face (`MODEL_PROVIDER=huggingface`)**
- `medical_zephyr` - Best quality, slower
- `medical_mistral` - Good balance
- `medical_llama2` - Popular choice
- `medical_openchat` - Fast responses

#### **Ollama (`MODEL_PROVIDER=ollama`)**
- `llama2` - General purpose
- `mistral` - Fast and efficient
- `medllama` - Medical specialized
- `codellama` - Technical understanding

#### **Free APIs (`MODEL_PROVIDER=free_api`)**
- `together` - Together AI service
- `groq` - Groq fast inference
- `perplexity` - Perplexity AI

## 🛠️ **Installation Guide**

### **Step 1: Basic Setup**
```bash
# Clone/navigate to your project
cd gp-medical-assistant

# Install Python dependencies
pip install -r requirements.txt
```

### **Step 2: Choose Your Model**

#### **Option A: Hugging Face (Cloud)**
```bash
# Copy configuration
cp .env.free .env

# Edit .env file
MODEL_PROVIDER=huggingface
MODEL_NAME=medical_zephyr
USE_GPU=false
```

#### **Option B: Ollama (Local)**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model
ollama pull llama2:7b

# Configure
echo "MODEL_PROVIDER=ollama" > .env
echo "MODEL_NAME=llama2" >> .env
```

#### **Option C: Free API**
```bash
# Get free API key from Together AI, Groq, etc.
echo "MODEL_PROVIDER=free_api" > .env
echo "MODEL_NAME=together" >> .env
echo "FREE_API_KEY=your_key_here" >> .env
```

### **Step 3: Run the Application**
```bash
python run_free.py
```

## 🎯 **Recommended Setups**

### **For Beginners**
```bash
MODEL_PROVIDER=huggingface
MODEL_NAME=medical_zephyr
USE_GPU=false
```
- Easy setup, no additional software
- Good quality responses
- Works on any computer

### **For Privacy/Offline**
```bash
MODEL_PROVIDER=ollama
MODEL_NAME=llama2
```
- Completely local
- No internet required after setup
- Full privacy control

### **For Performance**
```bash
MODEL_PROVIDER=free_api
MODEL_NAME=groq
FREE_API_KEY=your_groq_key
```
- Fastest responses
- High quality
- Free tier available

## 🔧 **Troubleshooting**

### **Common Issues**

#### **"Model not found" Error**
```bash
# For Hugging Face
pip install transformers torch

# For Ollama
ollama pull llama2:7b
```

#### **"Out of memory" Error**
```bash
# Use smaller model
MODEL_NAME=medical_mistral  # Instead of medical_llama2

# Or disable GPU
USE_GPU=false
```

#### **"API key invalid" Error**
```bash
# Check your API key
echo $FREE_API_KEY

# Get new key from provider website
```

### **Performance Tips**

1. **Use GPU** if available: `USE_GPU=true`
2. **Choose smaller models** for faster responses
3. **Use Ollama** for consistent local performance
4. **Use free APIs** for best quality without local resources

## 🌟 **Model Comparison**

| Aspect | Hugging Face | Ollama | Free APIs |
|--------|--------------|--------|-----------|
| **Setup** | Easy | Medium | Easy |
| **Privacy** | Medium | High | Low |
| **Speed** | Medium | Fast | Very Fast |
| **Quality** | High | High | Very High |
| **Cost** | Free | Free | Free Tier |
| **Offline** | No | Yes | No |

## 🚀 **Next Steps**

1. **Choose your preferred model** from the options above
2. **Configure your .env** file accordingly
3. **Run the application**: `python run_free.py`
4. **Test different models** to find your favorite
5. **Deploy to production** using the same configuration

## 💡 **Pro Tips**

- **Start with Zephyr-7B** for best quality
- **Use Ollama** if you want privacy
- **Try multiple models** to compare responses
- **Monitor resource usage** on your system
- **Keep fallback options** configured

Your GP Medical Assistant now works with **completely free AI models**! No more API costs! 🎉🤗