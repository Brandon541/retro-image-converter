#!/bin/bash

echo "🎮 Setting up Retro Image Converter..."
echo "=================================="

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Make the main script executable
chmod +x retro_converter.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "To use the tool:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the tool: python retro_converter.py [options] input.jpg output.png"
echo ""
echo "Or use the convenience script: ./run_converter.sh [options] input.jpg output.png"
echo ""
echo "For help: python retro_converter.py --help"
echo "For info: python retro_converter.py info"
