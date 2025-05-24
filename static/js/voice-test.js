// Simple Voice Detection Test
class VoiceTest {
    constructor() {
        this.audioContext = null;
        this.analyser = null;
        this.microphone = null;
        this.dataArray = null;
        this.isRunning = false;
    }

    async start() {
        try {
            console.log('Requesting microphone access...');
            this.microphone = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    sampleRate: 16000
                } 
            });
            
            console.log('Microphone access granted');
            
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            
            if (this.audioContext.state === 'suspended') {
                await this.audioContext.resume();
                console.log('Audio context resumed');
            }
            
            this.analyser = this.audioContext.createAnalyser();
            this.analyser.fftSize = 256;
            this.analyser.smoothingTimeConstant = 0.8;
            
            const source = this.audioContext.createMediaStreamSource(this.microphone);
            source.connect(this.analyser);
            
            const bufferLength = this.analyser.frequencyBinCount;
            this.dataArray = new Uint8Array(bufferLength);
            
            this.isRunning = true;
            this.monitor();
            
            console.log('Voice monitoring started. Speak into the microphone...');
            
        } catch (error) {
            console.error('Error starting voice test:', error);
        }
    }
    
    monitor() {
        if (!this.isRunning) return;
        
        this.analyser.getByteFrequencyData(this.dataArray);
        
        let sum = 0;
        for (let i = 0; i < this.dataArray.length; i++) {
            sum += this.dataArray[i];
        }
        const average = sum / this.dataArray.length;
        const max = Math.max(...this.dataArray);
        
        const voiceDetected = average > 15 || max > 50;
        
        if (voiceDetected) {
            console.log(`🎤 VOICE DETECTED - Avg: ${average.toFixed(2)}, Max: ${max}`);
        }
        
        // Update every 100ms
        setTimeout(() => this.monitor(), 100);
    }
    
    stop() {
        this.isRunning = false;
        
        if (this.microphone) {
            this.microphone.getTracks().forEach(track => track.stop());
        }
        
        if (this.audioContext) {
            this.audioContext.close();
        }
        
        console.log('Voice test stopped');
    }
}

// Test function to be called from browser console
window.testVoice = function() {
    if (window.voiceTest) {
        window.voiceTest.stop();
    }
    
    window.voiceTest = new VoiceTest();
    window.voiceTest.start();
    
    console.log('Voice test started. To stop, run: stopVoiceTest()');
};

window.stopVoiceTest = function() {
    if (window.voiceTest) {
        window.voiceTest.stop();
        window.voiceTest = null;
    }
};

console.log('Voice test utility loaded. Run testVoice() in console to start testing.'); 