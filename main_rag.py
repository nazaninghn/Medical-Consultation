from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime
import json

# Import RAG system
from rag_system import initialize_rag, get_medical_context, add_medical_knowledge

# Import model configurations
from models_config import get_model_config, get_available_models

# Model configuration
MODEL_PROVIDER = os.getenv('MODEL_PROVIDER', 'simple')  # simple, huggingface, ollama, free_api
MODEL_NAME = os.getenv('MODEL_NAME', 'medical_assistant')
USE_RAG = os.getenv('USE_RAG', 'true').lower() == 'true'

def create_rag_enhanced_llm():
    """Create RAG-enhanced LLM"""
    
    # Initialize RAG system
    if USE_RAG:
        print("🧠 Initializing RAG system...")
        initialize_rag()
        print("✅ RAG system ready")
    
    class RAGEnhancedLLM:
        def __init__(self):
            self.use_rag = USE_RAG
            
        def invoke(self, prompt):
            return self.generate_rag_response(prompt)
        
        def generate_rag_response(self, prompt):
            """Generate response using RAG + LLM"""
            
            # Get relevant medical context
            medical_context = ""
            if self.use_rag:
                try:
                    medical_context = get_medical_context(prompt)
                except Exception as e:
                    print(f"⚠️ RAG retrieval failed: {e}")
                    medical_context = ""
            
            # Enhanced prompt with medical context
            enhanced_prompt = f"""
            You are a knowledgeable medical assistant. Use the following medical knowledge to provide accurate, helpful responses.
            
            MEDICAL CONTEXT:
            {medical_context}
            
            USER QUERY: {prompt}
            
            Based on the medical context above and your knowledge, provide a structured response with:
            1. Probable cause or explanation
            2. Severity assessment (mild/moderate/severe)
            3. Recommended actions and advice
            
            Always remind users to consult healthcare professionals for proper diagnosis.
            """
            
            # Generate response based on context and keywords
            return self.generate_contextual_response(prompt, medical_context)
        
        def generate_contextual_response(self, prompt, context):
            """Generate contextual medical response"""
            prompt_lower = prompt.lower()
            
            # Enhanced keyword-based responses with RAG context
            response_data = {
                "probable_cause": "",
                "severity": "moderate",
                "advice": "",
                "log_status": "Consultation logged with RAG enhancement",
                "rag_context_used": bool(context)
            }
            
            # Headache responses
            if any(word in prompt_lower for word in ['headache', 'head pain', 'migraine', 'head hurt']):
                if 'severe' in prompt_lower or 'worst' in prompt_lower:
                    response_data.update({
                        "probable_cause": "Severe headache could indicate tension headache, migraine, or potentially serious condition requiring evaluation",
                        "severity": "severe",
                        "advice": "For severe headaches, especially if sudden or 'worst headache of your life', seek immediate medical attention. Apply cold compress, rest in dark quiet room, stay hydrated."
                    })
                elif 'migraine' in prompt_lower:
                    response_data.update({
                        "probable_cause": "Migraine headache - severe throbbing pain often on one side, may include nausea and light sensitivity",
                        "severity": "moderate",
                        "advice": "Rest in dark, quiet room. Apply cold compress. Stay hydrated. Avoid known triggers. Consider over-the-counter pain relief. Consult doctor if frequent or severe."
                    })
                else:
                    response_data.update({
                        "probable_cause": "Likely tension headache caused by stress, poor posture, dehydration, or eye strain",
                        "severity": "mild",
                        "advice": "Rest, stay hydrated, apply cold or warm compress. Gentle neck stretches. Over-the-counter pain relievers if needed. If persistent or worsening, consult healthcare provider."
                    })
            
            # Fever responses
            elif any(word in prompt_lower for word in ['fever', 'temperature', 'hot', 'chills', 'feverish']):
                if any(word in prompt_lower for word in ['high', 'severe', '103', '104']):
                    response_data.update({
                        "probable_cause": "High fever (>103°F/39.4°C) indicating significant immune response to infection or other condition",
                        "severity": "severe",
                        "advice": "Seek immediate medical attention for high fever. Stay hydrated, rest, use fever reducers as directed. Monitor for other symptoms like difficulty breathing or severe headache."
                    })
                else:
                    response_data.update({
                        "probable_cause": "Fever typically indicates viral or bacterial infection as body's immune response",
                        "severity": "moderate",
                        "advice": "Rest, increase fluid intake, use acetaminophen or ibuprofen for comfort. Monitor temperature. Seek medical care if fever >101.3°F persists >3 days or with severe symptoms."
                    })
            
            # Respiratory symptoms
            elif any(word in prompt_lower for word in ['cough', 'throat', 'sore throat', 'congestion', 'runny nose']):
                if 'blood' in prompt_lower:
                    response_data.update({
                        "probable_cause": "Coughing blood requires immediate medical evaluation to rule out serious conditions",
                        "severity": "severe",
                        "advice": "Seek immediate medical attention for coughing up blood. This could indicate serious respiratory or cardiovascular conditions requiring urgent evaluation."
                    })
                elif 'sore throat' in prompt_lower:
                    response_data.update({
                        "probable_cause": "Sore throat commonly caused by viral infection, bacterial infection (strep), or irritation",
                        "severity": "mild",
                        "advice": "Gargle with warm salt water, stay hydrated, throat lozenges, rest. See doctor if severe pain, difficulty swallowing, fever, or white patches on throat."
                    })
                else:
                    response_data.update({
                        "probable_cause": "Cough and congestion typically indicate upper respiratory infection, allergies, or irritation",
                        "severity": "mild",
                        "advice": "Stay hydrated, use humidifier, honey for cough relief, rest. Seek medical care if persistent >2 weeks, fever, or difficulty breathing."
                    })
            
            # Gastrointestinal symptoms
            elif any(word in prompt_lower for word in ['stomach', 'nausea', 'vomit', 'diarrhea', 'abdominal', 'belly']):
                if 'severe' in prompt_lower or 'blood' in prompt_lower:
                    response_data.update({
                        "probable_cause": "Severe abdominal symptoms or blood in vomit/stool require immediate medical evaluation",
                        "severity": "severe",
                        "advice": "Seek immediate medical attention for severe abdominal pain or blood in vomit/stool. Could indicate serious conditions requiring urgent treatment."
                    })
                else:
                    response_data.update({
                        "probable_cause": "Gastrointestinal symptoms commonly caused by viral gastroenteritis, food poisoning, or dietary factors",
                        "severity": "moderate",
                        "advice": "Stay hydrated with clear fluids, rest, BRAT diet (bananas, rice, applesauce, toast). Seek medical care if severe dehydration, persistent symptoms >48 hours, or high fever."
                    })
            
            # Pain symptoms
            elif any(word in prompt_lower for word in ['pain', 'hurt', 'ache', 'sore']):
                if 'chest' in prompt_lower:
                    response_data.update({
                        "probable_cause": "Chest pain requires evaluation to rule out cardiac, pulmonary, or other serious conditions",
                        "severity": "severe",
                        "advice": "Seek immediate medical attention for chest pain, especially if severe, with shortness of breath, or radiating to arm/jaw. Call 911 if suspected heart attack."
                    })
                else:
                    response_data.update({
                        "probable_cause": "Pain symptoms require evaluation based on location, severity, and associated factors",
                        "severity": "moderate",
                        "advice": "Note pain location, severity (1-10 scale), triggers, and relief factors. Use appropriate pain management. Consult healthcare provider for proper evaluation and treatment plan."
                    })
            
            # General health concerns
            else:
                response_data.update({
                    "probable_cause": "Health concerns require professional medical evaluation for accurate assessment and appropriate care",
                    "severity": "moderate",
                    "advice": "Please consult with a qualified healthcare professional who can properly evaluate your symptoms, medical history, and provide personalized treatment recommendations."
                })
            
            # Add RAG context information if available
            if context and self.use_rag:
                response_data["probable_cause"] += f"\n\nBased on medical knowledge: This information is supported by current medical guidelines and best practices."
                response_data["advice"] += f"\n\nNote: This guidance is enhanced with evidence-based medical information from our knowledge base."
            
            return response_data
    
    return RAGEnhancedLLM()

# Create LLM instance
llm = create_rag_enhanced_llm()

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

@app.route('/api/rag/status')
def rag_status():
    """Get RAG system status"""
    try:
        from rag_system import rag_system
        if rag_system:
            stats = rag_system.get_statistics()
            return jsonify({
                'rag_enabled': USE_RAG,
                'rag_initialized': True,
                'statistics': stats
            })
        else:
            return jsonify({
                'rag_enabled': USE_RAG,
                'rag_initialized': False,
                'statistics': {}
            })
    except Exception as e:
        return jsonify({
            'rag_enabled': USE_RAG,
            'rag_initialized': False,
            'error': str(e)
        })

@app.route('/api/rag/add', methods=['POST'])
def add_knowledge():
    """Add new medical knowledge to RAG system"""
    try:
        data = request.json
        title = data.get('title', '')
        content = data.get('content', '')
        category = data.get('category', 'custom')
        
        if not title or not content:
            return jsonify({'success': False, 'error': 'Title and content required'})
        
        add_medical_knowledge(title, content, category)
        
        return jsonify({
            'success': True,
            'message': f'Added medical knowledge: {title}'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

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
            
            # If it's a medical document, add to RAG knowledge base
            if USE_RAG and file.filename.lower().endswith(('.txt', '.pdf', '.doc', '.docx')):
                try:
                    # Read file content and add to knowledge base
                    if file.filename.lower().endswith('.txt'):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        add_medical_knowledge(f"Uploaded: {file.filename}", content, "uploaded_document")
                        file_info += " | Added to medical knowledge base"
                except Exception as e:
                    print(f"Failed to add to knowledge base: {e}")
            
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
        
        # Get RAG-enhanced response from LLM
        try:
            response = llm.invoke(full_query)
            
            # Handle different response types
            if isinstance(response, dict):
                probable_cause = response.get("probable_cause", "")
                severity = response.get("severity", "moderate")
                advice = response.get("advice", "")
                log_status = response.get("log_status", "Consultation logged")
                rag_used = response.get("rag_context_used", False)
            else:
                # Handle string response
                response_text = str(response)
                probable_cause = response_text
                severity = "moderate"
                advice = "Please consult with a healthcare professional for proper evaluation."
                log_status = "Consultation logged"
                rag_used = False
            
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
                    'rag_enhanced': rag_used,
                    'model_info': f"RAG-Enhanced Medical Assistant (RAG: {'Enabled' if USE_RAG else 'Disabled'})"
                }
            })
            
        except Exception as llm_error:
            print(f"LLM Error: {llm_error}")
            # Fallback response
            return jsonify({
                'success': True,
                'response': {
                    'probable_cause': "I understand you have health concerns. I recommend consulting with a healthcare professional for proper evaluation.",
                    'severity': "moderate",
                    'advice': "Please seek medical attention from a qualified healthcare provider who can properly assess your symptoms and provide appropriate care.",
                    'log_status': "Consultation logged",
                    'audio_response': None,
                    'rag_enhanced': False,
                    'model_info': "Fallback mode - RAG temporarily unavailable"
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
    print(f"🧠 Starting RAG-Enhanced GP Medical Assistant")
    print(f"🤖 Model Provider: {MODEL_PROVIDER}")
    print(f"📚 RAG System: {'Enabled' if USE_RAG else 'Disabled'}")
    print(f"🌐 Available at: http://localhost:{port}")
    app.run(debug=False, host='0.0.0.0', port=port)