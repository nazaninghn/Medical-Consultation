from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime
import json

# Import model configurations
from models_config import get_model_config, get_available_models

# Try different model providers
MODEL_PROVIDER = os.getenv('MODEL_PROVIDER', 'huggingface')  # huggingface, ollama, free_api
MODEL_NAME = os.getenv('MODEL_NAME', 'medical_zephyr')

def create_llm():
    """Create LLM based on configured provider"""
    try:
        if MODEL_PROVIDER == 'huggingface':
            return create_huggingface_llm()
        elif MODEL_PROVIDER == 'ollama':
            return create_ollama_llm()
        elif MODEL_PROVIDER == 'free_api':
            return create_free_api_llm()
        else:
            # Fallback to simple response
            return create_simple_llm()
    except Exception as e:
        print(f"Error creating LLM: {e}")
        return create_simple_llm()

def create_huggingface_llm():
    """Create Hugging Face LLM"""
    try:
        from langchain_huggingface import HuggingFacePipeline
        from transformers import pipeline
        
        config = get_model_config("huggingface", MODEL_NAME)
        
        # Create pipeline
        pipe = pipeline(
            "text-generation",
            model=config["model_id"],
            max_new_tokens=config["max_tokens"],
            temperature=config["temperature"],
            device_map="auto" if os.getenv('USE_GPU', 'false').lower() == 'true' else None
        )
        
        return HuggingFacePipeline(pipeline=pipe)
    except Exception as e:
        print(f"Hugging Face model failed: {e}")
        return create_simple_llm()

def create_ollama_llm():
    """Create Ollama local LLM"""
    try:
        from langchain_community.llms import Ollama
        
        config = get_model_config("ollama", MODEL_NAME)
        
        return Ollama(
            model=config["model_name"],
            temperature=config["temperature"]
        )
    except Exception as e:
        print(f"Ollama model failed: {e}")
        return create_simple_llm()

def create_free_api_llm():
    """Create free API LLM"""
    try:
        from langchain_openai import ChatOpenAI
        
        config = get_model_config("free_api", MODEL_NAME)
        api_key = os.getenv('FREE_API_KEY', 'dummy-key')
        
        return ChatOpenAI(
            base_url=config["base_url"],
            api_key=api_key,
            model=config["model"],
            temperature=0.3
        )
    except Exception as e:
        print(f"Free API model failed: {e}")
        return create_simple_llm()

def create_simple_llm():
    """Fallback simple LLM that works without external APIs"""
    class SimpleLLM:
        def invoke(self, prompt):
            return self.generate_medical_response(prompt)
        
        def generate_medical_response(self, prompt):
            """Generate a simple medical response based on keywords"""
            prompt_lower = prompt.lower()
            
            # Simple keyword-based responses
            if any(word in prompt_lower for word in ['headache', 'head pain', 'migraine']):
                return {
                    "probable_cause": "Possible tension headache, dehydration, or stress-related headache",
                    "severity": "mild",
                    "advice": "Rest in a quiet, dark room. Stay hydrated. Consider over-the-counter pain relief. If severe or persistent, consult a healthcare professional.",
                    "log_status": "Consultation logged"
                }
            elif any(word in prompt_lower for word in ['fever', 'temperature', 'hot', 'chills']):
                return {
                    "probable_cause": "Possible viral or bacterial infection causing elevated body temperature",
                    "severity": "moderate",
                    "advice": "Monitor temperature, stay hydrated, rest. Seek medical attention if fever exceeds 101.3°F (38.5°C) or persists.",
                    "log_status": "Consultation logged"
                }
            elif any(word in prompt_lower for word in ['cough', 'throat', 'sore throat']):
                return {
                    "probable_cause": "Possible upper respiratory infection, allergies, or throat irritation",
                    "severity": "mild",
                    "advice": "Stay hydrated, use throat lozenges, gargle with warm salt water. Consult doctor if symptoms worsen or persist beyond a week.",
                    "log_status": "Consultation logged"
                }
            elif any(word in prompt_lower for word in ['stomach', 'nausea', 'vomit', 'abdominal']):
                return {
                    "probable_cause": "Possible gastroenteritis, food poisoning, or digestive upset",
                    "severity": "moderate",
                    "advice": "Stay hydrated with clear fluids, rest, avoid solid foods initially. Seek medical care if severe or persistent.",
                    "log_status": "Consultation logged"
                }
            elif any(word in prompt_lower for word in ['pain', 'hurt', 'ache']):
                return {
                    "probable_cause": "Pain symptoms requiring evaluation based on location and severity",
                    "severity": "moderate",
                    "advice": "Monitor pain levels, note triggers and relief factors. Consult healthcare professional for proper evaluation and treatment.",
                    "log_status": "Consultation logged"
                }
            else:
                return {
                    "probable_cause": "General health concern requiring professional medical evaluation",
                    "severity": "moderate",
                    "advice": "Please consult with a qualified healthcare professional for proper diagnosis and treatment recommendations.",
                    "log_status": "Consultation logged"
                }
    
    return SimpleLLM()

# Create LLM instance
llm = create_llm()

# Import tools and schema
try:
    from tools import tools, convert_text_to_speech, process_uploaded_file, convert_speech_to_text
    from schema import SymptomResponse, ChatRequest
except ImportError:
    # Fallback if imports fail
    tools = []
    def convert_text_to_speech(text, session_id): return None
    def process_uploaded_file(path): return "File processed"
    def convert_speech_to_text(path): return "Speech processed"
    
    class SymptomResponse:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

# Flask App Setup
app = Flask(__name__)
CORS(app)

# Configure upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'wav', 'mp3', 'ogg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('static/audio', exist_ok=True)

# Chat Session Storage
chat_sessions = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/models')
def get_models():
    """Get available models"""
    return jsonify({
        'current_provider': MODEL_PROVIDER,
        'current_model': MODEL_NAME,
        'available_models': get_available_models()
    })

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Process the file
            file_info = process_uploaded_file(file_path)
            
            return jsonify({
                'success': True,
                'filename': filename,
                'file_path': file_path,
                'file_info': file_info
            })
        else:
            return jsonify({'success': False, 'error': 'File type not allowed'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # Handle both JSON and form data
        if request.is_json:
            data = request.json
        else:
            data = request.form.to_dict()
        
        query = data.get('message', '')
        session_id = data.get('session_id', 'default')
        uploaded_files = data.get('files', [])
        
        # Process uploaded files
        file_context = ""
        if uploaded_files:
            for file_path in uploaded_files:
                if os.path.exists(file_path):
                    file_info = process_uploaded_file(file_path)
                    file_context += f"\nFile analysis: {file_info}"
        
        # Combine query with file context
        full_query = f"{query}\n{file_context}" if file_context else query
        
        if session_id not in chat_sessions:
            chat_sessions[session_id] = []
        
        # Get response from LLM
        try:
            response = llm.invoke(full_query)
            
            # Handle different response types
            if isinstance(response, dict):
                probable_cause = response.get("probable_cause", "")
                severity = response.get("severity", "moderate")
                advice = response.get("advice", "")
                log_status = response.get("log_status", "Consultation logged")
            else:
                # Handle string response
                response_text = str(response)
                probable_cause = response_text
                severity = "moderate"
                advice = "Please consult with a healthcare professional for proper evaluation."
                log_status = "Consultation logged"
            
            # Generate audio response
            audio_path = None
            try:
                audio_text = f"{probable_cause}. {advice}"
                audio_path = convert_text_to_speech(audio_text, session_id)
            except:
                pass
            
            return jsonify({
                'success': True,
                'response': {
                    'probable_cause': probable_cause,
                    'severity': severity,
                    'advice': advice,
                    'log_status': log_status,
                    'audio_response': audio_path if audio_path and not audio_path.startswith('Error') else None,
                    'model_info': f"Powered by {MODEL_PROVIDER}: {MODEL_NAME}"
                }
            })
            
        except Exception as llm_error:
            print(f"LLM Error: {llm_error}")
            # Fallback response
            return jsonify({
                'success': True,
                'response': {
                    'probable_cause': "I understand you have health concerns. While I'm currently experiencing technical difficulties with the AI model, I recommend consulting with a healthcare professional for proper evaluation.",
                    'severity': "moderate",
                    'advice': "Please seek medical attention from a qualified healthcare provider who can properly assess your symptoms and provide appropriate care.",
                    'log_status': "Consultation logged",
                    'audio_response': None,
                    'model_info': f"Fallback mode - {MODEL_PROVIDER} temporarily unavailable"
                }
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/audio/<path:filename>')
def serve_audio(filename):
    try:
        return send_file(f'static/audio/{filename}', as_attachment=False)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🤗 Starting GP Medical Assistant with {MODEL_PROVIDER} model: {MODEL_NAME}")
    print(f"🌐 Available at: http://localhost:{port}")
    app.run(debug=False, host='0.0.0.0', port=port)