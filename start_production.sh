#!/bin/bash
echo "🚀 Starting Imperial Network 2.0 Production Server"
echo "=================================================="
echo "📍 Running on: http://0.0.0.0:8000"
echo "📍 Public URL: https://api.humbu.store"
echo "=================================================="

# Start with gunicorn (4 workers for better performance)
gunicorn -w 4 -b 0.0.0.0:8000 app:app
