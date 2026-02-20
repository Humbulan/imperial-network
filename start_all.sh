#!/bin/bash

echo "🏛️ IMPERIAL NETWORK 2.0 - COMPLETE SYSTEM STARTUP"
echo "=================================================="
echo ""

# Step 1: Check environment
echo "📋 Step 1: Checking environment..."
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    exit 1
fi
echo "✅ Environment OK"

# Step 2: Check database
echo "📋 Step 2: Checking database..."
if [ ! -f "instance/imperial.db" ]; then
    echo "🆕 Creating fresh database..."
    python -c "from app import app, db; app.app_context().push(); db.create_all()"
fi
echo "✅ Database OK"

# Step 3: Populate with sample data (optional)
echo "📋 Step 3: Would you like to populate with sample data? (y/n)"
read -r answer
if [ "$answer" = "y" ]; then
    echo "📊 Populating database..."
    python populate_data.py
fi

# Step 4: Start monitoring in background
echo "📋 Step 4: Starting API monitor..."
nohup python monitor_api.py > monitor.log 2>&1 &
echo "✅ Monitor started (PID: $!)"

# Step 5: Start production server
echo ""
echo "🚀 Step 5: Starting production server..."
echo "=================================================="
echo "📍 Local URL: http://localhost:8000"
echo "📍 Public URL: https://api.humbu.store"
echo "📍 Monitor: http://localhost:8000/monitor"
echo "=================================================="
echo ""

# Start gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
