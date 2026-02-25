#!/bin/bash
# Quick start for Water Restructuring Dashboard

echo "🌊 Water Restructuring Frequency Sweep Dashboard"
echo "=================================================="
echo ""

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.9+"
    exit 1
fi

echo "📦 Installing/checking dependencies..."
pip install -q -r requirements.txt 2>/dev/null

echo ""
echo "🚀 Starting Streamlit dashboard..."
echo "   Open your browser to: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the dashboard"
echo ""

streamlit run streamlit_app.py
