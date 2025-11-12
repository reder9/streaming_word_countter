"""
Vosk-based Jabroni Counter - Offline, highly accurate speech recognition
Install with: pip install vosk requests
"""

import json
import threading
import time
import os
import pyaudio
import wave
import re
from datetime import datetime
import requests
import zipfile
import difflib

try:
    import vosk
    VOSK_AVAILABLE = True
except ImportError:
    VOSK_AVAILABLE = False

class VoskJabroniCounter:
    def __init__(self):
        if not VOSK_AVAILABLE:
            print("❌ Vosk not available. Install with: pip install vosk")
            print("   This version provides much better offline accuracy!")
            return
            
        self.count = 0
        self.target_words = [
            "jabroni", "jabrone", "jabroney", "jaboni", "jaboney",
            "gibron", "gibrone", "gibroni", "giboney",
            "jibron", "jibrone", "jibroni", "jiboney",
            "jabro", "gibro", "jibro"
        ]
        
        self.model_path = "vosk-model-small-en-us-0.15"
        self.setup_vosk_model()
        
        # Audio settings optimized for speech recognition
        self.rate = 16000
        self.chunk = 8192
        self.channels = 1
        self.format = pyaudio.paInt16
        
        self.is_listening = False
        self.html_file = "jabroni_counter.html"
        self.last_detection_time = 0
        self.detection_cooldown = 2
        
        print("🎯 Vosk-based Jabroni Counter initialized!")
        print(f"🔍 Monitoring for: {', '.join(self.target_words[:6])}...")
    
    def setup_vosk_model(self):
        """Download and setup Vosk model if not exists"""
        if not os.path.exists(self.model_path):
            print("📦 Downloading Vosk speech model (first time only)...")
            print("   This may take a few minutes but greatly improves accuracy...")
            
            model_url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
            model_zip = "vosk-model.zip"
            
            try:
                # Download model
                response = requests.get(model_url, stream=True)
                total_size = int(response.headers.get('content-length', 0))
                
                with open(model_zip, 'wb') as f:
                    downloaded = 0
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"\r   Progress: {percent:.1f}%", end="", flush=True)
                
                print(f"\n✅ Model downloaded successfully!")
                
                # Extract model
                with zipfile.ZipFile(model_zip, 'r') as zip_ref:
                    zip_ref.extractall(".")
                
                os.remove(model_zip)
                print("✅ Model extracted and ready!")
                
            except Exception as e:
                print(f"❌ Error downloading model: {e}")
                print("   Please check your internet connection and try again.")
                return False
                
        try:
            self.model = vosk.Model(self.model_path)
            print("✅ Vosk model loaded successfully!")
            return True
        except Exception as e:
            print(f"❌ Error loading Vosk model: {e}")
            return False
    
    def find_all_jabronis_in_text(self, heard_text, confidence_threshold=0.6):
        """Find ALL jabroni instances in a sentence - handles multiple jabronis"""
        heard_lower = heard_text.lower().strip()
        matches = []
        
        # Special patterns for common Vosk mis-hearings of "jabroni"
        jabroni_patterns = [
            # Two-word patterns that sound like "jabroni"
            (r'(jeb|job|chub|cheb|jab|geb|gib)\s+(ron|ronnie|roni|broni|brone)', 'jabroni'),
            (r'(gibber|gibbon|jabber)\s+(ron|ronnie|roni)', 'jabroni'),
            (r'(job|jeb|jab|gab|gib)\s+(bron|bronnie|brony)', 'jabroni'),
            
            # Single word patterns
            (r'jabronny|jabrony|jebroni|gibroni|jabbroni', 'jabroni'),
            (r'gibronny|gibrony|jobronny|jebrony', 'jabroni'),
        ]
        
        # Find all pattern matches first
        for pattern, target in jabroni_patterns:
            pattern_matches = list(re.finditer(pattern, heard_lower))
            for match in pattern_matches:
                matches.append({
                    'word': match.group(),
                    'target': target,
                    'confidence': 0.95,
                    'method': 'pattern',
                    'position': match.span()
                })
                print(f"🎯 Pattern match: '{match.group()}' → '{target}'")
        
        # Remove already matched portions to avoid double-counting
        remaining_text = heard_lower
        for match in sorted(matches, key=lambda x: x['position'][0], reverse=True):
            start, end = match['position']
            remaining_text = remaining_text[:start] + ' ' * (end - start) + remaining_text[end:]
        
        # Check for direct word matches in remaining text
        words = remaining_text.split()
        for i, word in enumerate(words):
            if word.strip() == '':  # Skip blanked out portions
                continue
                
            clean_word = ''.join(c for c in word if c.isalnum())
            if len(clean_word) < 3:
                continue
                
            for target in self.target_words:
                # Direct substring matching
                if target in clean_word or clean_word in target:
                    matches.append({
                        'word': word,
                        'target': target,
                        'confidence': 1.0,
                        'method': 'direct',
                        'position': None
                    })
                    print(f"🎯 Direct match: '{word}' → '{target}'")
                    break
                
                # Fuzzy matching
                similarity = difflib.SequenceMatcher(None, clean_word, target).ratio()
                if similarity >= confidence_threshold:
                    matches.append({
                        'word': word,
                        'target': target,
                        'confidence': similarity,
                        'method': 'fuzzy',
                        'position': None
                    })
                    print(f"🎯 Fuzzy match: '{word}' → '{target}' ({similarity:.2f})")
                    break
        
        return matches
    
    def listen_for_words_vosk(self):
        """Listen using Vosk for better accuracy"""
        if not hasattr(self, 'model'):
            print("❌ Vosk model not loaded!")
            return
            
        recognizer = vosk.KaldiRecognizer(self.model, self.rate)
        recognizer.SetWords(True)  # Enable word-level timestamps
        
        # Setup audio stream
        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        
        print("🎙️ Vosk listening started... (much better accuracy!)")
        self.is_listening = True
        
        try:
            while self.is_listening:
                data = stream.read(self.chunk, exception_on_overflow=False)
                
                if recognizer.AcceptWaveform(data):
                    # Final result
                    result = json.loads(recognizer.Result())
                    if 'text' in result and result['text']:
                        self.process_vosk_result(result)
                else:
                    # Partial result (real-time)
                    partial = json.loads(recognizer.PartialResult())
                    if 'partial' in partial and partial['partial']:
                        # You could process partial results here for even faster response
                        pass
                        
        except Exception as e:
            print(f"❌ Vosk listening error: {e}")
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()
    
    def process_vosk_result(self, result):
        """Process Vosk recognition result with enhanced jabroni detection"""
        text = result.get('text', '').lower()
        confidence = result.get('confidence', 1.0) if 'confidence' in result else 1.0
        
        if not text:
            return
            
        print(f"🎤 [VOSK] Heard: '{text}' (confidence: {confidence:.2f})")
        
        # Find ALL jabroni matches in the text (handles multiple jabronis per sentence)
        matches = self.find_all_jabronis_in_text(text, 0.6)
        
        if matches:
            # Check cooldown
            current_time = time.time()
            if current_time - self.last_detection_time < self.detection_cooldown:
                print(f"⏰ Cooldown active, skipping detection")
                return
                
            # Count all matches found
            jabroni_count = len(matches)
            self.count += jabroni_count
            self.last_detection_time = current_time
            
            print(f"🎉 JABRONI{'S' if jabroni_count > 1 else ''} DETECTED! (Vosk Enhanced)")
            print(f"   📝 Original: '{text}'")
            
            for i, match in enumerate(matches, 1):
                method = 'Pattern' if match['confidence'] >= 0.9 else 'Fuzzy'
                print(f"   🎯 Match #{i}: '{match['word']}' → '{match['target']}' ({match['confidence']:.2f}) [{method}]")
            
            print(f"   � Found {jabroni_count} jabroni{'s' if jabroni_count > 1 else ''} in this sentence!")
            print(f"   🔢 Total count: {self.count}")
            
            if jabroni_count > 1:
                print(f"   💥 MULTIPLE JABRONIS DETECTED! That's a jabroni bonanza!")
            
            self.update_html()
            self.save_count()
        else:
            # Debug output for tuning
            if any(word in text for word in ['jeb', 'job', 'chub', 'ron', 'bron', 'jab', 'gib']):
                print(f"🔍 Close but no match: '{text}'")
    
    def update_html(self):
        """Update HTML with Vosk branding"""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vosk Jabroni Counter</title>
    <style>
        body {{
            font-family: 'Arial Black', Arial, sans-serif;
            background: transparent;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            color: white;
        }}
        .counter-container {{
            text-align: center;
            background: rgba(0, 20, 40, 0.9);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0, 100, 200, 0.3);
            backdrop-filter: blur(10px);
            border: 2px solid rgba(100, 200, 255, 0.4);
        }}
        .title {{
            font-size: 2.5em;
            margin-bottom: 5px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
            color: #64C8FF;
        }}
        .vosk-badge {{
            font-size: 0.7em;
            color: #4ECDC4;
            margin-bottom: 15px;
            opacity: 0.9;
        }}
        .count {{
            font-size: 8em;
            font-weight: bold;
            color: #64C8FF;
            text-shadow: 0 0 20px #64C8FF;
            margin: 20px 0;
            transition: all 0.3s ease;
        }}
        .count.flash {{
            animation: voskFlash 1.8s ease-in-out;
        }}
        .subtitle {{
            font-size: 1.5em;
            opacity: 0.9;
            margin-top: 20px;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
        }}
        
        @keyframes voskFlash {{
            0% {{ 
                transform: scale(1); 
                color: #64C8FF;
                text-shadow: 0 0 20px #64C8FF;
            }}
            20% {{ 
                transform: scale(1.4); 
                color: #FF6B6B;
                text-shadow: 0 0 40px #FF6B6B, 0 0 80px #FF6B6B;
            }}
            40% {{ 
                transform: scale(1.3); 
                color: #4ECDC4;
                text-shadow: 0 0 35px #4ECDC4, 0 0 70px #4ECDC4;
            }}
            60% {{ 
                transform: scale(1.35); 
                color: #FFD93D;
                text-shadow: 0 0 40px #FFD93D, 0 0 80px #FFD93D;
            }}
            80% {{ 
                transform: scale(1.2); 
                color: #6BCF7F;
                text-shadow: 0 0 30px #6BCF7F, 0 0 60px #6BCF7F;
            }}
            100% {{ 
                transform: scale(1); 
                color: #64C8FF;
                text-shadow: 0 0 20px #64C8FF;
            }}
        }}
    </style>
    <script>
        function checkForNewDetection() {{
            const currentCount = {self.count};
            const lastCount = localStorage.getItem('lastJabroniCount') || '0';
            
            if (parseInt(currentCount) > parseInt(lastCount)) {{
                const countElement = document.querySelector('.count');
                countElement.classList.add('flash');
                
                setTimeout(() => {{
                    countElement.classList.remove('flash');
                }}, 1800);
                
                localStorage.setItem('lastJabroniCount', currentCount.toString());
            }}
            
            setTimeout(() => {{
                window.location.reload();
            }}, 1500);
        }}
        
        window.onload = checkForNewDetection;
    </script>
</head>
<body>
    <div class="counter-container">
        <div class="title">JABRONI COUNTER</div>
        <div class="count">{self.count}</div>
        <div class="subtitle">Jabronis Detected</div>
    </div>
</body>
</html>
"""
        
        with open(self.html_file, 'w') as f:
            f.write(html_content)
    
    def save_count(self):
        """Save count with Vosk metadata"""
        data = {
            'count': self.count,
            'last_updated': datetime.now().isoformat(),
            'engine': 'vosk',
            'model': self.model_path
        }
        with open('jabroni_data.json', 'w') as f:
            json.dump(data, f, indent=2)
    
    def start(self):
        """Start Vosk counter"""
        self.count = 0
        print(f"🔄 Vosk counter reset to 0")
        
        self.update_html()
        self.save_count()
        
        listen_thread = threading.Thread(target=self.listen_for_words_vosk)
        listen_thread.daemon = True
        listen_thread.start()
        
        print("🚀 Vosk Jabroni Counter running!")
        print("✨ Features: Offline recognition, high accuracy, real-time processing")
        print("🎯 Detection cooldown: 2 seconds")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping Vosk Jabroni Counter...")
            self.is_listening = False

if __name__ == "__main__":
    counter = VoskJabroniCounter()
    if hasattr(counter, 'model'):
        counter.start()
    else:
        print("Please install Vosk: pip install vosk requests")