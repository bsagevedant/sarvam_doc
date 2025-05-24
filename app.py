from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import os
import io
import tempfile
from werkzeug.utils import secure_filename
from config import Config
from sarvam_client import SarvamAIClient
from medical_ai import MedicalAI

app = Flask(__name__)
CORS(app)

# Initialize clients
sarvam_client = None
medical_ai = MedicalAI()

def init_sarvam_client():
    """Initialize Sarvam AI client"""
    global sarvam_client
    api_key = Config.SARVAM_API_KEY
    if not api_key:
        print("Warning: SARVAM_API_KEY not found in environment variables")
        return False
    
    sarvam_client = SarvamAIClient(api_key)
    return True

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html', 
                         languages=Config.LANGUAGE_NAMES,
                         supported_languages=Config.SUPPORTED_LANGUAGES)

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Multilingual AI Doctor Agent is running',
        'sarvam_client_ready': sarvam_client is not None
    })

@app.route('/api/consult', methods=['POST'])
def text_consultation():
    """Text-based medical consultation"""
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'Query is required'}), 400
        
        query = data['query'].strip()
        if not query:
            return jsonify({'error': 'Query cannot be empty'}), 400
        
        # Detect language
        detected_language = 'en'
        if sarvam_client:
            detected_language = sarvam_client.detect_language(query) or 'en'
        
        # Generate medical response
        response = medical_ai.generate_medical_response(query, detected_language)
        
        # Translate response if requested language is different
        requested_language = data.get('language', detected_language)
        if requested_language != detected_language and sarvam_client:
            translated_response = sarvam_client.translate_text(
                response, 
                requested_language, 
                detected_language
            )
            if translated_response:
                response = translated_response
        
        return jsonify({
            'success': True,
            'response': response,
            'detected_language': detected_language,
            'response_language': requested_language,
            'language_name': Config.LANGUAGE_NAMES.get(detected_language, 'Unknown')
        })
    
    except Exception as e:
        print(f"Error in text consultation: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/audio-consult', methods=['POST'])
def audio_consultation():
    """Audio-based medical consultation"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'Audio file is required'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'error': 'No audio file selected'}), 400
        
        if not sarvam_client:
            return jsonify({'error': 'Sarvam AI client not initialized'}), 500
        
        # Save audio file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            audio_file.save(temp_file.name)
            temp_file_path = temp_file.name
        
        try:
            # Convert speech to text
            transcript = sarvam_client.speech_to_text(temp_file_path)
            if not transcript:
                return jsonify({'error': 'Could not transcribe audio'}), 400
            
            # Detect language from transcript
            detected_language = sarvam_client.detect_language(transcript) or 'en'
            
            # Generate medical response
            response = medical_ai.generate_medical_response(transcript, detected_language)
            
            # Convert response to speech
            audio_response = sarvam_client.text_to_speech(response, detected_language)
            
            result = {
                'success': True,
                'transcript': transcript,
                'response': response,
                'detected_language': detected_language,
                'language_name': Config.LANGUAGE_NAMES.get(detected_language, 'Unknown'),
                'has_audio_response': audio_response is not None
            }
            
            # If audio response is available, save it and provide download link
            if audio_response:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as audio_temp:
                    audio_temp.write(audio_response)
                    result['audio_response_url'] = f'/api/download-audio/{os.path.basename(audio_temp.name)}'
            
            return jsonify(result)
        
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    except Exception as e:
        print(f"Error in audio consultation: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/download-audio/<filename>')
def download_audio(filename):
    """Download generated audio response"""
    try:
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'Audio file not found'}), 404
        
        return send_file(file_path, as_attachment=True, download_name='response.wav')
    
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/translate', methods=['POST'])
def translate_text():
    """Translate text to different language"""
    try:
        data = request.get_json()
        if not data or 'text' not in data or 'target_language' not in data:
            return jsonify({'error': 'Text and target_language are required'}), 400
        
        if not sarvam_client:
            return jsonify({'error': 'Translation service not available'}), 500
        
        text = data['text']
        target_language = data['target_language']
        source_language = data.get('source_language', 'auto')
        
        translated_text = sarvam_client.translate_text(text, target_language, source_language)
        
        return jsonify({
            'success': True,
            'original_text': text,
            'translated_text': translated_text,
            'source_language': source_language,
            'target_language': target_language
        })
    
    except Exception as e:
        print(f"Error in translation: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/detect-language', methods=['POST'])
def detect_language():
    """Detect language of input text"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400
        
        if not sarvam_client:
            return jsonify({'error': 'Language detection service not available'}), 500
        
        text = data['text']
        detected_lang = sarvam_client.detect_language(text)
        
        return jsonify({
            'success': True,
            'text': text,
            'detected_language': detected_lang,
            'language_name': Config.LANGUAGE_NAMES.get(detected_lang, 'Unknown')
        })
    
    except Exception as e:
        print(f"Error in language detection: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Initialize Sarvam client
    if not init_sarvam_client():
        print("Warning: Running without Sarvam AI integration")
    
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Create static directory if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')
    
    app.run(
        host='0.0.0.0',
        port=Config.PORT,
        debug=Config.FLASK_ENV == 'development'
    ) 