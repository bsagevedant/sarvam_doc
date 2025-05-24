# 🏥 Dr. Sarvam - Multilingual AI Doctor Agent

A comprehensive AI-powered medical consultation system that can communicate with patients across India in their native languages using Sarvam AI APIs.

## 🌟 Features

### 🗣️ Multilingual Communication
- **Automatic Language Detection**: Detects the patient's language automatically
- **11+ Indian Languages**: Hindi, Bengali, Telugu, Tamil, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Odia, and English
- **Real-time Translation**: Seamless translation between languages using Sarvam AI's Mayura model

### 🎤 Voice & Text Interaction
- **Speech-to-Text**: Convert patient's voice to text using Sarvam AI's Saarika ASR model
- **Text-to-Speech**: Generate audio responses using Sarvam AI's Bulbul TTS model
- **Audio Visualization**: Real-time audio visualization during recording
- **Text Chat**: Traditional text-based consultation interface

### 🚨 Medical Intelligence
- **Symptom Detection**: Advanced pattern matching for common symptoms
- **Emergency Detection**: Automatic detection of emergency situations
- **Medical Knowledge Base**: Built-in medical knowledge for common health issues
- **Cultural Sensitivity**: Culturally appropriate responses for Indian patients
- **Follow-up Questions**: Intelligent follow-up questions for better diagnosis

### 🔧 Technical Features
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time Processing**: Fast response times with efficient API integration
- **Audio Recording**: High-quality audio recording with noise cancellation
- **Modern UI**: Beautiful, medical-themed user interface
- **Error Handling**: Comprehensive error handling and user feedback

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Sarvam AI API Key ([Get one here](https://www.sarvam.ai/))
- Modern web browser with microphone support

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd akashvani_sarvam
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
# Copy the example file and edit it
cp env_example.txt .env

# Edit .env file and add your Sarvam AI API key
SARVAM_API_KEY=your_sarvam_ai_api_key_here
PORT=5000
FLASK_ENV=development
```

4. **Run the application**
```bash
python app.py
```

5. **Open in browser**
Navigate to `http://localhost:5000`

## 🏗️ Architecture

### Backend Components
- **Flask Web Server**: Main application server
- **Sarvam AI Client**: Integration with Sarvam AI APIs
- **Medical AI Engine**: Medical knowledge processing and symptom detection
- **Configuration Management**: Environment-based configuration

### Frontend Components
- **Responsive Web UI**: Bootstrap-based responsive interface
- **Audio Recording**: WebRTC-based audio capture and visualization
- **Real-time Chat**: Dynamic chat interface with message handling
- **Language Support**: Multi-language UI elements and indicators

### Sarvam AI Integration
- **ASR (Saarika)**: Speech-to-text conversion
- **TTS (Bulbul)**: Text-to-speech synthesis
- **Translation (Mayura)**: Language translation
- **Language Detection**: Automatic language identification

## 📋 API Endpoints

### Health Check
```
GET /api/health
```
Returns API health status and Sarvam client readiness.

### Text Consultation
```
POST /api/consult
Content-Type: application/json

{
    "query": "मुझे सिरदर्द हो रहा है",
    "language": "hi"  // optional
}
```

### Audio Consultation
```
POST /api/audio-consult
Content-Type: multipart/form-data

audio: <audio_file>
```

### Language Detection
```
POST /api/detect-language
Content-Type: application/json

{
    "text": "Hello, how are you?"
}
```

### Translation
```
POST /api/translate
Content-Type: application/json

{
    "text": "Hello",
    "target_language": "hi",
    "source_language": "en"
}
```

## 🌐 Supported Languages

| Language | Code | Native Name |
|----------|------|-------------|
| Hindi | hi | हिंदी |
| Bengali | bn | বাংলা |
| Telugu | te | తెలుగు |
| Tamil | ta | தமிழ் |
| Marathi | mr | मराठी |
| Gujarati | gu | ગુજરાતી |
| Kannada | kn | ಕನ್ನಡ |
| Malayalam | ml | മലയാളം |
| Punjabi | pa | ਪੰਜਾਬੀ |
| Odia | or | ଓଡ଼ିଆ |
| English | en | English |

## 🏥 Medical Features

### Symptom Detection
The system can detect and respond to various symptoms:
- Fever and temperature-related issues
- Headaches and migraines
- Cough and respiratory problems
- Stomach pain and digestive issues
- Common cold and flu symptoms

### Emergency Detection
Automatic detection of emergency keywords in multiple languages:
- Chest pain / सीने में दर्द
- Difficulty breathing / सांस लेने में तकलीफ
- Unconscious / बेहोशी
- Severe bleeding / खून बहना
- Heart attack / हार्ट अटैक

### Medical Responses
- **Symptom Analysis**: Understanding and categorizing symptoms
- **Possible Causes**: Listing potential causes for symptoms
- **General Advice**: Providing safe, general medical guidance
- **Emergency Indicators**: Clear indicators when to seek immediate help
- **Follow-up Questions**: Intelligent questions for better assessment

## 🔧 Configuration

### Environment Variables
```bash
SARVAM_API_KEY=your_api_key_here    # Required: Sarvam AI API key
PORT=5000                           # Optional: Server port (default: 5000)
FLASK_ENV=development               # Optional: Flask environment
```

### Customization
- **Medical Knowledge**: Edit `medical_ai.py` to add more medical conditions
- **Language Support**: Modify `config.py` to add more languages
- **UI Themes**: Customize `static/css/style.css` for different themes
- **Audio Settings**: Adjust audio parameters in `static/js/app.js`

## 🚨 Important Disclaimers

### Medical Disclaimer
⚠️ **This AI assistant provides general medical information only.**
- Always consult qualified healthcare professionals for proper diagnosis and treatment
- This system is not a replacement for professional medical advice
- In case of emergency, contact your local emergency services immediately (108/102 in India)

### Privacy & Security
- Audio recordings are processed in real-time and not stored permanently
- Patient conversations are not logged or saved
- All communications are processed securely through Sarvam AI APIs

## 🛠️ Development

### Project Structure
```
akashvani_sarvam/
├── app.py                 # Main Flask application
├── config.py             # Configuration and constants
├── sarvam_client.py      # Sarvam AI API client
├── medical_ai.py         # Medical consultation logic
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html        # Main web interface
├── static/
│   ├── css/
│   │   └── style.css     # Custom styles
│   └── js/
│       └── app.js        # Frontend JavaScript
└── README.md             # This file
```

### Adding New Features
1. **New Medical Conditions**: Add to `medical_knowledge` in `medical_ai.py`
2. **New Languages**: Update `SUPPORTED_LANGUAGES` in `config.py`
3. **UI Components**: Modify HTML templates and CSS
4. **API Endpoints**: Add new routes in `app.py`

### Testing
```bash
# Run the application in development mode
FLASK_ENV=development python app.py

# Test API endpoints
curl -X GET http://localhost:5000/api/health
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Sarvam AI** for providing excellent multilingual AI APIs
- **Bootstrap** for the responsive UI framework
- **Font Awesome** for the beautiful icons
- **Flask** for the lightweight web framework

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the [Sarvam AI documentation](https://docs.sarvam.ai/)
- Review the API health endpoint at `/api/health`

---

**Made with ❤️ for healthcare accessibility across India** 🇮🇳 