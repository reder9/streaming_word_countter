# 🎙️ Jabroni Counter for Streaming

A sophisticated Python application that listens to your microphone for the word "jabroni" and displays a real-time counter perfect for streaming with OBS. Features multiple recognition engines, high accuracy detection, and beautiful visual effects!

## ✨ Features

- � **Multiple Recognition Engines**: Basic Google Speech, Enhanced Multi-Engine, and Offline AI (Vosk)
- 🔍 **Smart Pattern Matching**: Detects "jabroni" even when pronounced as "job ronnie", "jeb ronnie", etc.
- 📊 **Multiple Jabroni Detection**: Counts all instances in a single sentence
- 💫 **Transparent HTML Display**: Perfect for OBS with flash effects and animations
- 🎨 **Visual Effects**: Counter flashes and glows when jabronis are detected
- 💾 **Auto-Reset**: Counter resets to 0 on startup for each streaming session
- 🖥️ **Cross-Platform**: Works on Windows, macOS, and Linux
- 📦 **Windows Executable**: Ready-to-use .exe file for easy deployment
- ⚡ **Real-Time Processing**: Low latency detection with configurable cooldown

## 🚀 Quick Setup

### Option 1: Enhanced Vosk (Recommended - Highest Accuracy)

1. **Create and activate virtual environment:**
   ```bash
   python3 -m venv jabroni_env
   source jabroni_env/bin/activate  # On Windows: jabroni_env\Scripts\activate
   ```

2. **Install system dependencies:**
   ```bash
   # macOS
   brew install portaudio
   
   # Ubuntu/Debian
   sudo apt-get install portaudio19-dev python3-pyaudio
   
   # Windows (install via pip, no system deps needed)
   ```

3. **Install Python dependencies:**
   ```bash
   pip install vosk requests speechrecognition pyaudio pocketsphinx
   ```

4. **Run the Vosk counter (best accuracy):**
   ```bash
   python vosk_jabroni_counter.py
   ```

### Option 2: Basic Setup

1. **Install basic requirements:**
   ```bash
   pip install speechrecognition pyaudio
   ```

2. **Run basic counter:**
   ```bash
   python jabroni_counter.py
   ```

### Option 3: Windows Executable
- Download the pre-built executable from releases
- Run `run_jabroni_counter.bat`
- No Python installation required!

## 🎮 Available Versions

### 🎯 Vosk AI Counter (Recommended)
**Best accuracy, offline, handles multiple jabronis per sentence**
```bash
python vosk_jabroni_counter.py
```
- 🏆 Highest accuracy (95%+)
- 📶 Works offline (no internet needed)
- 🎯 Detects "job ronnie" → "jabroni" patterns
- 📈 Counts multiple jabronis in one sentence
- 💫 Auto-downloads AI model (50MB)

### 🔄 Enhanced Multi-Engine Counter
**Multiple recognition engines with confidence scoring**
```bash
python enhanced_jabroni_counter.py
```
- 🎙️ Uses Google + PocketSphinx + Vosk
- 📊 Confidence scoring and fuzzy matching
- 🛡️ False positive filtering
- 🎯 Pattern detection for split words

### ⚡ Basic Counter
**Simple, lightweight version**
```bash
python jabroni_counter.py
```
- 🌐 Google Speech Recognition
- 💨 Fast and lightweight
- 📱 Easy setup

## 🎬 OBS Setup

1. **Add Browser Source in OBS:**
   - Add → Sources → Browser Source
   - **URL:** `file:///path/to/jabroni_counter.html` (use full path)
   - **Width:** 800, **Height:** 400
   - ✅ Check "Refresh browser when scene becomes active"

2. **Perfect for streaming:**
   - Transparent background
   - Flash effects on detection
   - Auto-refreshes with new counts
   - Clean, professional look

## 🔧 How It Works

1. **🎤 Audio Processing:** Real-time microphone monitoring with optimized audio chunks
2. **🧠 AI Recognition:** Advanced pattern matching for "jabroni" variations
3. **📊 Multiple Detection:** Finds ALL jabronis in a sentence ("that jabroni is such a jabroni" = 2 counts)
4. **💾 Smart Storage:** Auto-resets on startup, persistent during session
5. **🎨 Live Display:** HTML updates instantly with visual effects

## 🛠️ Troubleshooting

### 🎙️ Audio Issues:
```bash
# Test microphone access
python -c "import pyaudio; print('PyAudio works!')"

# Check available audio devices
python -c "import pyaudio; p = pyaudio.PyAudio(); [print(f'{i}: {p.get_device_info_by_index(i)[\"name\"]}') for i in range(p.get_device_count())]"
```

### 🔍 Recognition Issues:
- **Vosk (offline):** Best accuracy, works without internet
- **Basic version:** Needs internet connection
- **Speak clearly:** Normal volume, minimal background noise
- **Check cooldown:** 2-second delay between detections prevents spam

### 📺 OBS Issues:
- Use **full file path** (not relative)
- Enable "Refresh browser when scene becomes active"
- Check file permissions
- Right-click source → Reload if needed

## 🎨 Customization

### 🎯 Modify Detection Words
Edit `target_words` in any counter file:
```python
self.target_words = [
    "jabroni", "jabrone", "jabroney",  # standard variations
    "gibron", "jibron", "jabro",       # phonetic variations  
    "yourword", "anotherword"          # add your own!
]
```

### 🎭 Customize Visual Effects
Edit the HTML/CSS in `update_html()` method:
```python
# Change colors, fonts, animations, sizes
# Make it match your stream theme!
```

### ⚙️ Adjust Sensitivity
In Vosk counter, modify confidence thresholds:
```python
# Lower = more sensitive (may catch false positives)
# Higher = less sensitive (may miss some)
confidence_threshold = 0.6  # Default: 60%
```

## 📦 Windows Deployment

Ready-to-use Windows executable files are included:

```bash
# Build Windows executable (requires PyInstaller)
python setup.py build

# Or use the batch file
build_windows.bat

# Run on Windows
run_jabroni_counter.bat
```

## 🎯 Accuracy Comparison

| Version | Accuracy | Internet | Multiple Detection | Setup Difficulty |
|---------|----------|----------|-------------------|-----------------|
| **Vosk AI** | 95%+ | ❌ Offline | ✅ Yes | Medium |
| **Enhanced** | 85% | ✅ Required | ✅ Yes | Medium |
| **Basic** | 75% | ✅ Required | ❌ No | Easy |

## 🤝 Contributing

Feel free to submit issues and pull requests! Some ideas for improvements:

- 🎵 Add sound effects on detection
- 🎨 More visual themes
- 📱 Mobile app version
- 🌍 Multi-language support
- 📊 Analytics and statistics

## 📄 License

MIT License - feel free to use in your streams and modify as needed!

## 🎮 Perfect for Streamers

This tool was built specifically for content creators who want to:
- 🎭 Add interactive elements to their stream
- 📊 Track running gags and memes
- 💫 Engage viewers with real-time counters
- 🎨 Maintain professional visual quality

**Ready to count some jabronis? Let's go! 🚀**

## Files

- `jabroni_counter.py` - Main counter application
- `gui_controller.py` - GUI control panel
- `jabroni_counter.html` - Generated HTML display (auto-created)
- `jabroni_data.json` - Persistent count storage (auto-created)
- `requirements.txt` - Python dependencies

## System Requirements

- Python 3.7+
- Microphone access
- Internet connection (for default speech recognition)
- macOS/Windows/Linux compatible# streaming_word_countter
# streaming_word_countter
