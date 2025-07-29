# 🩺 GP Medical Assistant Chatbot

A beautiful, luxurious web-based medical assistant chatbot designed for general practitioner consultations. This AI-powered assistant helps users understand their symptoms and provides guidance on when to seek medical care.

**Developed by Nazanin** - Advanced Medical Consultation System

## ✨ Features

- **Beautiful UI**: Luxurious design with gold, navy, and emerald color scheme
- **Medical Consultation**: AI-powered symptom analysis and guidance
- **Severity Assessment**: Categorizes symptoms as mild, moderate, or severe
- **Professional Advice**: Provides recommendations for next steps
- **Session Logging**: Automatically logs consultations for record-keeping
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Medical Disclaimer**: Clear disclaimers about AI limitations

## 🎨 Design

The interface features a luxurious color palette:
- **Primary Gold**: Elegant gold gradients for user messages and accents
- **Navy Blue**: Professional navy backgrounds for headers
- **Emerald Green**: Medical-themed green for bot responses and severity indicators
- **Cream & Light Gray**: Soft, comfortable background colors

## 🚀 Quick Start

### 1. Setup
```bash
python setup.py
```

### 2. Configure API Key
1. Get your Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Edit the `.env` file and replace `your_google_gemini_api_key_here` with your actual API key

### 3. Run the Application
```bash
python run.py
```

### 4. Open in Browser
Navigate to `http://localhost:5000` in your web browser

## 📁 Project Structure

```
gp-medical-assistant/
├── main.py              # Main Flask application
├── run.py               # Application runner with checks
├── setup.py             # Setup script
├── schema.py            # Pydantic models for responses
├── tools.py             # LangChain tools for logging and resources
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
├── .env                 # Your environment variables (created by setup)
├── templates/
│   └── index.html       # Beautiful frontend interface
└── logs/                # Consultation logs (created automatically)
```

## 🔧 Manual Installation

If you prefer to set up manually:

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env and add your Google Gemini API key
# GOOGLE_API_KEY=your_actual_api_key_here

# Create logs directory
mkdir logs

# Run the application
python run.py
```

## 🩺 How It Works

1. **User Input**: Users describe their symptoms in natural language
2. **AI Analysis**: Google Gemini AI analyzes the symptoms using medical knowledge
3. **Structured Response**: The system provides:
   - Probable cause of symptoms
   - Severity level (mild/moderate/severe)
   - Recommended next steps
4. **Logging**: All consultations are automatically logged with timestamps
5. **Medical Resources**: Emergency contacts and resources are available

## ⚠️ Important Medical Disclaimer

This AI assistant provides general health information only and is **NOT** a substitute for professional medical advice, diagnosis, or treatment. 

- Always consult with qualified healthcare professionals
- Seek immediate medical attention for emergencies
- This tool does not provide medical diagnoses
- Use this information as guidance only

## 🛠️ Technical Details

- **Backend**: Flask web framework with LangChain integration
- **AI Model**: Google Gemini 2.5 Flash for medical consultations
- **Frontend**: Pure HTML/CSS/JavaScript with modern design
- **Data Validation**: Pydantic models for structured responses
- **Logging**: JSON-formatted consultation logs
- **CORS**: Enabled for cross-origin requests

## 📝 API Endpoints

### POST /api/chat
Processes user messages and returns medical guidance.

**Request:**
```json
{
  "message": "I have a headache and feel dizzy",
  "session_id": "optional_session_id"
}
```

**Response:**
```json
{
  "success": true,
  "response": {
    "probable_cause": "Possible tension headache or dehydration",
    "severity": "mild",
    "advice": "Rest, hydrate, and monitor symptoms. Consult a doctor if symptoms persist.",
    "log_status": "Consultation logged successfully"
  }
}
```

## 🔒 Privacy & Security

- No personal health information is stored permanently
- Session data is kept in memory only
- Consultation logs contain only symptom descriptions and timestamps
- All communications are processed securely

## 🤝 Contributing

This is a medical assistant tool. Please ensure any contributions:
- Maintain medical accuracy and safety
- Include appropriate disclaimers
- Follow medical ethics guidelines
- Test thoroughly before deployment

## 📄 License

This project is for educational and demonstration purposes. Please ensure compliance with medical software regulations in your jurisdiction before using in production.

---

**Remember**: This tool is designed to assist and educate, not to replace professional medical care. Always consult with healthcare professionals for medical concerns.

## 👩‍💻 **Developer**

**Nazanin** - Full Stack Developer & AI Enthusiast

- 🩺 **Specialized in**: Medical AI Applications
- 🚀 **Technologies**: Python, Flask, LangChain, Google Gemini AI
- 💡 **Focus**: Healthcare Technology & User Experience
- 🌟 **Mission**: Making healthcare more accessible through AI

---

*© 2025 Nazanin - GP Medical Assistant. Crafted with ❤️ and cutting-edge AI technology.*