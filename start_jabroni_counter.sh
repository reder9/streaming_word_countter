#!/bin/bash
# Vosk Jabroni Counter Startup Script
# Automatically sets up and runs the best accuracy counter

echo "🎙️ Starting Vosk Jabroni Counter..."
echo "✨ High accuracy offline speech recognition"
echo ""

# Activate virtual environment if it exists
if [ -d "jabroni_env" ]; then
    echo "📦 Activating virtual environment..."
    source jabroni_env/bin/activate
else
    echo "⚠️  No virtual environment found. Run setup first:"
    echo "   python3 -m venv jabroni_env"
    echo "   source jabroni_env/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Check if requirements are installed
echo "🔍 Checking dependencies..."
python -c "import vosk, speechrecognition, pyaudio" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing dependencies. Installing..."
    pip install -r requirements.txt
fi

echo "🚀 Starting Vosk Jabroni Counter (press Ctrl+C to stop)..."
echo "📺 Open jabroni_counter.html in OBS as Browser Source"
echo ""

# Start the counter
python vosk_jabroni_counter.py