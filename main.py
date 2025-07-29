from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.messages import HumanMessage, AIMessage
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from datetime import datetime

from tools import tools, convert_text_to_speech, process_uploaded_file, convert_speech_to_text
from schema import SymptomResponse, ChatRequest

SYSTEM_PROMPT = """
You are a helpful medical assistant for a General Practitioner clinic. You do NOT give diagnoses.
You help users reflect on their symptoms and provide guidance.

For each consultation, provide:
1. A probable cause or explanation for the symptoms
2. Severity level: mild, moderate, or severe
3. Advice on next steps and whether to see a doctor

IMPORTANT: 
- Always be cautious and refer to doctors when unclear
- Never provide definitive diagnoses
- Always recommend consulting healthcare professionals for proper medical advice
- Call the log_symptom_entry tool to record the consultation

Respond in a helpful, professional manner while being clear about limitations.
"""

# Gemini LLM Setup
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.3,
    max_output_tokens=1000
)

# JSON Output Parser
parser = PydanticOutputParser(pydantic_object=SymptomResponse)

# Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("placeholder", "{chat_history}"),
    ("human", "{query}"),
    ("placeholder", "{agent_scratchpad}")
])

# Agent & Executor
agent = create_tool_calling_agent(llm=llm, prompt=prompt, tools=tools)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

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
        audio_input = data.get('audio_input')
        
        # Process audio input if provided
        if audio_input:
            audio_text = convert_speech_to_text(audio_input)
            query = f"{query} {audio_text}" if query else audio_text
        
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
        
        chat_history = chat_sessions[session_id]
        chat_history.append(HumanMessage(content=full_query))
        
        result = executor.invoke({
            "query": full_query,
            "chat_history": chat_history
        })
        
        # Extract the response text
        response_text = result.get("output", "")
        chat_history.append(AIMessage(content=response_text))
        
        # Try to parse structured response, fallback to simple response
        try:
            # Try to parse as structured JSON
            response = parser.parse(response_text)
            probable_cause = response.probable_cause
            severity = response.severity
            advice = response.advice
            log_status = response.log_status
        except:
            # Fallback: create a simple structured response
            probable_cause = response_text
            severity = "moderate"  # Default severity
            advice = "Please consult with a healthcare professional for proper evaluation and treatment."
            log_status = "Consultation logged"
        
        # Generate audio response
        audio_text = f"{probable_cause}. {advice}"
        audio_path = convert_text_to_speech(audio_text, session_id)
        
        return jsonify({
            'success': True,
            'response': {
                'probable_cause': probable_cause,
                'severity': severity,
                'advice': advice,
                'log_status': log_status,
                'audio_response': audio_path if not audio_path.startswith('Error') else None
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
    app.run(debug=False, host='0.0.0.0', port=port)
