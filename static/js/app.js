// Multilingual AI Doctor Agent - Frontend JavaScript

class AIDoctor {
    constructor() {
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
        this.audioBlob = null;
        this.currentStream = null;
        this.loadingModal = null;
        
        // Voice conversation state
        this.conversationMode = false;
        this.isListening = false;
        this.voiceActivityDetector = null;
        this.silenceTimer = null;
        this.silenceThreshold = 2000; // 2 seconds of silence
        this.audioContext = null;
        this.analyser = null;
        this.dataArray = null;
        this.lastSpeechTime = 0;
        this.conversationActive = false;
        
        this.initializeElements();
        this.setupEventListeners();
        this.checkPermissions();
    }
    
    initializeElements() {
        // Chat elements
        this.chatMessages = document.getElementById('chatMessages');
        this.textInput = document.getElementById('textInput');
        this.sendTextBtn = document.getElementById('sendText');
        
        // Audio elements
        this.recordBtn = document.getElementById('recordBtn');
        this.stopBtn = document.getElementById('stopBtn');
        this.playBtn = document.getElementById('playBtn');
        this.sendAudioBtn = document.getElementById('sendAudio');
        this.audioCanvas = document.getElementById('audioCanvas');
        this.audioVisual = document.getElementById('audioVisual');
        
        // Conversation mode elements
        this.conversationModeBtn = document.getElementById('conversationMode');
        this.conversationStatus = document.getElementById('conversationStatus');
        this.voiceIndicator = document.getElementById('voiceIndicator');
        this.voiceLevelBar = document.getElementById('voiceLevelBar');
        
        // Form elements
        this.responseLanguage = document.getElementById('responseLanguage');
        this.detectedLanguage = document.getElementById('detectedLanguage');
        
        // Modal
        this.loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
        this.loadingText = document.getElementById('loadingText');
    }
    
    setupEventListeners() {
        // Text input
        this.sendTextBtn.addEventListener('click', () => this.sendTextMessage());
        this.textInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendTextMessage();
            }
        });
        
        // Audio controls
        this.recordBtn.addEventListener('click', () => this.startRecording());
        this.stopBtn.addEventListener('click', () => this.stopRecording());
        this.playBtn.addEventListener('click', () => this.playRecording());
        this.sendAudioBtn.addEventListener('click', () => this.sendAudioMessage());
        
        // Conversation mode
        if (this.conversationModeBtn) {
            this.conversationModeBtn.addEventListener('click', () => this.toggleConversationMode());
        }
    }
    
    async checkPermissions() {
        try {
            const permission = await navigator.permissions.query({ name: 'microphone' });
            if (permission.state === 'denied') {
                this.showError('Microphone permission is required for voice consultation.');
            }
        } catch (error) {
            console.log('Permission check not supported:', error);
        }
    }
    
    // Text Messaging
    async sendTextMessage() {
        const query = this.textInput.value.trim();
        if (!query) return;
        
        this.addMessage(query, 'user');
        this.textInput.value = '';
        this.showLoading('Processing your consultation...');
        
        try {
            const response = await fetch('/api/consult', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    query: query,
                    language: this.responseLanguage.value === 'auto' ? null : this.responseLanguage.value
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.addMessage(data.response, 'bot', data.detected_language);
                this.updateDetectedLanguage(data.detected_language, data.language_name);
                
                // Check if emergency response
                if (data.response.includes('🚨') || data.response.includes('EMERGENCY')) {
                    this.handleEmergencyResponse();
                }
            } else {
                throw new Error(data.error || 'Failed to get response');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showError('Sorry, there was an error processing your request. Please try again.');
        } finally {
            this.hideLoading();
        }
    }
    
    // Audio Recording
    async startRecording() {
        try {
            this.currentStream = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    sampleRate: 16000
                } 
            });
            
            this.mediaRecorder = new MediaRecorder(this.currentStream, {
                mimeType: 'audio/webm;codecs=opus'
            });
            
            this.audioChunks = [];
            
            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    this.audioChunks.push(event.data);
                }
            };
            
            this.mediaRecorder.onstop = () => {
                this.audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
                this.playBtn.disabled = false;
                this.sendAudioBtn.disabled = false;
                this.stopAudioVisualization();
            };
            
            this.mediaRecorder.start(100); // Collect data every 100ms
            this.isRecording = true;
            this.updateRecordingUI(true);
            this.startAudioVisualization();
            
        } catch (error) {
            console.error('Error starting recording:', error);
            this.showError('Could not start recording. Please check microphone permissions.');
        }
    }
    
    stopRecording() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.currentStream.getTracks().forEach(track => track.stop());
            this.isRecording = false;
            this.updateRecordingUI(false);
        }
    }
    
    playRecording() {
        if (this.audioBlob) {
            const audio = new Audio(URL.createObjectURL(this.audioBlob));
            audio.play();
        }
    }
    
    async sendAudioMessage() {
        if (!this.audioBlob) return;
        
        this.showLoading('Transcribing and processing your voice...');
        
        try {
            const formData = new FormData();
            formData.append('audio', this.audioBlob, 'recording.webm');
            
            const response = await fetch('/api/audio-consult', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Add user message (transcript)
                this.addMessage(`🎤 ${data.transcript}`, 'user');
                
                // Add bot response
                this.addMessage(data.response, 'bot', data.detected_language);
                this.updateDetectedLanguage(data.detected_language, data.language_name);
                
                // Add audio response if available
                if (data.has_audio_response && data.audio_response_url) {
                    await this.addAudioResponse(data.audio_response_url);
                }
                
                // Check for emergency
                if (data.response.includes('🚨') || data.response.includes('EMERGENCY')) {
                    this.handleEmergencyResponse();
                }
                
                // In conversation mode, restart listening after response
                if (this.conversationMode) {
                    this.updateConversationStatus('Speaking...');
                    setTimeout(() => {
                        this.continueConversation();
                    }, 1000); // Wait 1 second before listening again
                }
                
                // Reset audio controls
                this.resetAudioControls();
                
            } else {
                throw new Error(data.error || 'Failed to process audio');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showError('Sorry, there was an error processing your audio. Please try again.');
        } finally {
            this.hideLoading();
        }
    }
    
    // Audio Visualization
    startAudioVisualization() {
        this.audioVisual.style.display = 'block';
        const canvas = this.audioCanvas;
        const canvasCtx = canvas.getContext('2d');
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const analyser = audioContext.createAnalyser();
        const source = audioContext.createMediaStreamSource(this.currentStream);
        
        source.connect(analyser);
        analyser.fftSize = 256;
        
        const bufferLength = analyser.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);
        
        const draw = () => {
            if (!this.isRecording) return;
            
            requestAnimationFrame(draw);
            analyser.getByteFrequencyData(dataArray);
            
            canvasCtx.fillStyle = '#f8f9fa';
            canvasCtx.fillRect(0, 0, canvas.width, canvas.height);
            
            const barWidth = (canvas.width / bufferLength) * 2.5;
            let barHeight;
            let x = 0;
            
            for (let i = 0; i < bufferLength; i++) {
                barHeight = (dataArray[i] / 255) * canvas.height;
                
                const gradient = canvasCtx.createLinearGradient(0, canvas.height - barHeight, 0, canvas.height);
                gradient.addColorStop(0, '#dc3545');
                gradient.addColorStop(1, '#ff6b6b');
                
                canvasCtx.fillStyle = gradient;
                canvasCtx.fillRect(x, canvas.height - barHeight, barWidth, barHeight);
                
                x += barWidth + 1;
            }
        };
        
        draw();
    }
    
    stopAudioVisualization() {
        this.audioVisual.style.display = 'none';
    }
    
    // UI Updates
    addMessage(content, type, language = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        if (content.includes('🚨')) {
            messageDiv.classList.add('emergency-message');
        }
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        if (type === 'user') {
            messageContent.innerHTML = `<i class="fas fa-user"></i><strong>You:</strong><br>${content}`;
        } else {
            messageContent.innerHTML = `<i class="fas fa-robot"></i><strong>Dr. Sarvam:</strong><br>${content}`;
            if (language) {
                messageContent.innerHTML += `<span class="language-detected">${this.getLanguageName(language)}</span>`;
            }
        }
        
        messageDiv.appendChild(messageContent);
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    async addAudioResponse(audioUrl) {
        const audioDiv = document.createElement('div');
        audioDiv.className = 'audio-player';
        audioDiv.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fas fa-volume-up me-2"></i>
                <span class="me-3">Audio Response:</span>
                <audio controls ${this.conversationMode ? 'autoplay' : ''}>
                    <source src="${audioUrl}" type="audio/wav">
                    Your browser does not support audio playback.
                </audio>
            </div>
        `;
        this.chatMessages.appendChild(audioDiv);
        this.scrollToBottom();
        
        // In conversation mode, wait for audio to finish before continuing
        if (this.conversationMode) {
            const audio = audioDiv.querySelector('audio');
            return new Promise((resolve) => {
                audio.addEventListener('ended', () => {
                    resolve();
                });
                audio.addEventListener('error', () => {
                    resolve(); // Continue even if audio fails
                });
                // Timeout fallback in case audio doesn't load
                setTimeout(resolve, 30000);
            });
        }
    }
    
    updateRecordingUI(isRecording) {
        if (isRecording) {
            this.recordBtn.disabled = true;
            this.recordBtn.classList.add('recording');
            this.stopBtn.disabled = false;
            this.playBtn.disabled = true;
            this.sendAudioBtn.disabled = true;
        } else {
            this.recordBtn.disabled = false;
            this.recordBtn.classList.remove('recording');
            this.stopBtn.disabled = true;
        }
    }
    
    resetAudioControls() {
        this.audioBlob = null;
        this.audioChunks = [];
        this.playBtn.disabled = true;
        this.sendAudioBtn.disabled = true;
        this.updateRecordingUI(false);
    }
    
    updateDetectedLanguage(langCode, langName) {
        this.detectedLanguage.value = `${langName} (${langCode})`;
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    showLoading(text = 'Processing...') {
        this.loadingText.textContent = text;
        this.loadingModal.show();
    }
    
    hideLoading() {
        this.loadingModal.hide();
    }
    
    showError(message) {
        this.addMessage(`❌ Error: ${message}`, 'bot');
    }
    
    handleEmergencyResponse() {
        // Add visual emergency indicators
        document.body.style.animation = 'emergencyBlink 1s infinite';
        
        // Auto-hide the emergency animation after 10 seconds
        setTimeout(() => {
            document.body.style.animation = '';
        }, 10000);
        
        // Show emergency alert
        const alertDiv = document.createElement('div');
        alertDiv.className = 'emergency-alert';
        alertDiv.innerHTML = `
            <div class="text-center">
                <i class="fas fa-exclamation-triangle fa-2x mb-2"></i>
                <h5>MEDICAL EMERGENCY DETECTED</h5>
                <p>If this is a life-threatening emergency, please call 108/102 immediately!</p>
            </div>
        `;
        
        this.chatMessages.insertBefore(alertDiv, this.chatMessages.lastChild);
        this.scrollToBottom();
    }
    
    getLanguageName(code) {
        const languages = {
            'hi': 'हिंदी',
            'bn': 'বাংলা',
            'te': 'తెలుగు',
            'ta': 'தமிழ்',
            'mr': 'मराठी',
            'gu': 'ગુજરાતી',
            'kn': 'ಕನ್ನಡ',
            'ml': 'മലയാളം',
            'pa': 'ਪੰਜਾਬੀ',
            'or': 'ଓଡ଼ିଆ',
            'en': 'English'
        };
        return languages[code] || code;
    }
    
    async toggleConversationMode() {
        this.conversationMode = !this.conversationMode;
        
        if (this.conversationMode) {
            // Check microphone permissions first
            try {
                await navigator.mediaDevices.getUserMedia({ audio: true });
                
                this.conversationModeBtn.innerHTML = '<i class="fas fa-stop"></i> Stop Conversation';
                this.conversationModeBtn.className = 'btn btn-danger me-2';
                this.updateConversationStatus('Starting...');
                
                // Add user guidance
                this.addMessage('🎤 Conversation mode activated! Speak naturally and I\'ll respond. The system will automatically detect when you start and stop talking.', 'bot');
                
                await this.startListening();
            } catch (error) {
                console.error('Microphone permission denied:', error);
                this.conversationMode = false;
                this.showError('Microphone permission is required for conversation mode. Please allow microphone access and try again.');
            }
        } else {
            this.conversationModeBtn.innerHTML = '<i class="fas fa-comments"></i> Start 2-Way Conversation';
            this.conversationModeBtn.className = 'btn btn-primary me-2';
            this.updateConversationStatus('Inactive');
            this.stopListening();
            
            this.addMessage('Conversation mode deactivated. You can use manual recording or text input.', 'bot');
        }
    }
    
    async startListening() {
        if (!this.conversationMode) return;
        
        try {
            // Get microphone access if not already available
            if (!this.currentStream) {
                this.currentStream = await navigator.mediaDevices.getUserMedia({ 
                    audio: {
                        echoCancellation: true,
                        noiseSuppression: true,
                        sampleRate: 16000
                    } 
                });
            }
            
            this.isListening = true;
            this.conversationActive = true;
            this.lastSpeechTime = Date.now();
            
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            
            // Resume audio context if needed (required by modern browsers)
            if (this.audioContext.state === 'suspended') {
                await this.audioContext.resume();
            }
            
            this.analyser = this.audioContext.createAnalyser();
            this.analyser.fftSize = 256;
            this.analyser.smoothingTimeConstant = 0.8;
            
            const bufferLength = this.analyser.frequencyBinCount;
            this.dataArray = new Uint8Array(bufferLength);
            
            const source = this.audioContext.createMediaStreamSource(this.currentStream);
            source.connect(this.analyser);
            
            this.updateConversationStatus('Listening...');
            this.startAudioVisualization();
            
            console.log('Starting voice activity detector...');
            this.voiceActivityDetector = setInterval(() => {
                this.checkVoiceActivity();
            }, 100);
            
        } catch (error) {
            console.error('Error starting conversation mode:', error);
            this.showError('Could not start conversation mode. Please check microphone permissions.');
            this.conversationMode = false;
            this.updateConversationStatus('Inactive');
        }
    }
    
    async startConversationRecording() {
        try {
            // Initialize MediaRecorder for conversation mode
            if (!this.mediaRecorder || this.mediaRecorder.state === 'inactive') {
                this.mediaRecorder = new MediaRecorder(this.currentStream, {
                    mimeType: 'audio/webm;codecs=opus'
                });
                
                this.audioChunks = [];
                
                this.mediaRecorder.ondataavailable = (event) => {
                    if (event.data.size > 0) {
                        this.audioChunks.push(event.data);
                    }
                };
                
                this.mediaRecorder.onstop = () => {
                    this.audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
                    console.log('Recording stopped, audio blob created:', this.audioBlob.size);
                };
            }
            
            if (this.mediaRecorder.state === 'inactive') {
                this.mediaRecorder.start(100);
                this.isRecording = true;
                this.updateRecordingUI(true);
                console.log('MediaRecorder started for conversation');
            }
            
        } catch (error) {
            console.error('Error starting conversation recording:', error);
        }
    }
    
    stopListening() {
        console.log('Stopping conversation mode listening...');
        this.isListening = false;
        this.conversationActive = false;
        
        // Stop any ongoing recording
        if (this.isRecording) {
            this.stopRecording();
        }
        
        // Clear voice activity detector
        if (this.voiceActivityDetector) {
            clearInterval(this.voiceActivityDetector);
            this.voiceActivityDetector = null;
        }
        
        // Close audio context
        if (this.audioContext && this.audioContext.state !== 'closed') {
            this.audioContext.close();
            this.audioContext = null;
        }
        
        // Stop microphone stream
        if (this.currentStream) {
            this.currentStream.getTracks().forEach(track => track.stop());
            this.currentStream = null;
        }
        
        this.updateRecordingUI(false);
        this.stopAudioVisualization();
    }
    
    checkVoiceActivity() {
        if (!this.analyser || !this.dataArray || !this.conversationMode) return;
        
        this.analyser.getByteFrequencyData(this.dataArray);
        
        // Calculate average volume
        let sum = 0;
        for (let i = 0; i < this.dataArray.length; i++) {
            sum += this.dataArray[i];
        }
        const average = sum / this.dataArray.length;
        
        // Also calculate max volume for better detection
        let max = Math.max(...this.dataArray);
        
        // Lower voice activity threshold for better detection
        const voiceThreshold = 15; // Reduced from 30
        const maxThreshold = 50;   // Additional max threshold
        
        // Voice detected if average OR max exceeds threshold
        const voiceDetected = average > voiceThreshold || max > maxThreshold;
        
        // Update voice level indicator
        this.updateVoiceLevelIndicator(average, max, voiceDetected);
        
        console.log(`Voice Detection - Avg: ${average.toFixed(2)}, Max: ${max}, Detected: ${voiceDetected}, Recording: ${this.isRecording}`);
        
        if (voiceDetected) {
            this.lastSpeechTime = Date.now();
            
            // If not currently recording, start recording
            if (!this.isRecording && this.conversationMode && this.conversationActive) {
                console.log('Starting recording due to voice detection');
                this.startConversationRecording();
            }
        } else {
            // Check for silence timeout
            const currentTime = Date.now();
            const timeSinceLastSpeech = currentTime - this.lastSpeechTime;
            
            if (timeSinceLastSpeech > this.silenceThreshold && this.isRecording) {
                console.log('Stopping recording due to silence timeout');
                this.stopRecording();
                this.updateConversationStatus('Processing...');
                setTimeout(() => {
                    this.sendAudioMessage();
                }, 100);
            }
        }
    }
    
    continueConversation() {
        if (!this.conversationMode) return;
        
        // Restart listening for the next user input
        this.conversationActive = true;
        this.lastSpeechTime = Date.now();
        this.updateConversationStatus('Listening...');
    }
    
    updateConversationStatus(status) {
        if (this.conversationStatus) {
            this.conversationStatus.textContent = `Conversation Mode: ${status}`;
            
            // Remove all status classes
            this.conversationStatus.classList.remove('conversation-listening', 'conversation-processing', 'conversation-speaking');
            
            // Add appropriate class based on status
            if (status === 'Listening...' || status === 'Active') {
                this.conversationStatus.classList.add('conversation-listening');
            } else if (status === 'Processing...' || status === 'Starting...') {
                this.conversationStatus.classList.add('conversation-processing');
            } else if (status === 'Speaking...') {
                this.conversationStatus.classList.add('conversation-speaking');
            }
        }
        
        // Show/hide voice indicator
        if (this.voiceIndicator) {
            if (status === 'Listening...' && this.conversationMode) {
                this.voiceIndicator.style.display = 'block';
            } else {
                this.voiceIndicator.style.display = 'none';
            }
        }
        
        // Update audio controls container styling
        const audioControls = document.querySelector('.audio-controls');
        if (audioControls && this.conversationMode) {
            audioControls.classList.add('conversation-mode-active');
        } else if (audioControls) {
            audioControls.classList.remove('conversation-mode-active');
        }
    }
    
    updateVoiceLevelIndicator(average, max, voiceDetected) {
        if (!this.voiceLevelBar) return;
        
        // Scale the voice level (0-100)
        const level = Math.min(100, (Math.max(average, max) / 128) * 100);
        this.voiceLevelBar.style.width = `${level}%`;
        
        // Add visual feedback for voice detection
        if (voiceDetected) {
            this.voiceLevelBar.classList.add('voice-detecting');
        } else {
            this.voiceLevelBar.classList.remove('voice-detecting');
        }
    }
}

// Utility Functions
function checkAPIHealth() {
    fetch('/api/health')
        .then(response => response.json())
        .then(data => {
            console.log('API Health:', data);
        })
        .catch(error => {
            console.error('API Health Check Failed:', error);
        });
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Check for required features
    if (!('MediaRecorder' in window)) {
        console.warn('MediaRecorder not supported. Audio features will be limited.');
        document.querySelector('.audio-controls').style.display = 'none';
    }
    
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        console.warn('Speech Recognition not supported.');
    }
    
    // Initialize the main application
    const aiDoctor = new AIDoctor();
    
    // Check API health
    checkAPIHealth();
    
    // Add welcome message animation
    setTimeout(() => {
        const welcomeMessage = document.querySelector('.bot-message');
        if (welcomeMessage) {
            welcomeMessage.style.transform = 'scale(1.02)';
            setTimeout(() => {
                welcomeMessage.style.transform = 'scale(1)';
            }, 200);
        }
    }, 500);
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + Enter to send message
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            aiDoctor.sendTextMessage();
        }
        
        // Space to start/stop recording (when not typing)
        if (e.code === 'Space' && e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
            e.preventDefault();
            if (aiDoctor.isRecording) {
                aiDoctor.stopRecording();
            } else {
                aiDoctor.startRecording();
            }
        }
    });
    
    // Add service worker registration for offline support
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/js/sw.js')
            .then(registration => {
                console.log('ServiceWorker registered:', registration);
            })
            .catch(error => {
                console.log('ServiceWorker registration failed:', error);
            });
    }
}); 