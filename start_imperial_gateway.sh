#!/data/data/com.termux/files/usr/bin/bash

echo "🏛️ IMPERIAL GATEWAY STARTUP"
echo "==========================="
cd ~/imperial_network

# Kill any existing processes
pkill -f "python3.*app.py"
pkill -f "portal_master_8088.py"
pkill -f "imperial_proxy_8080.py"

# Start the core engine (Port 8000)
echo "Starting Imperial Engine (Port 8000)..."
nohup python3 app.py > logs/engine.log 2>&1 &

# Start the high-quality frontend (Port 8088)
echo "Starting Imperial Portal (Port 8088)..."
nohup python3 portal_master_8088.py > logs/portal.log 2>&1 &

# Start the unified proxy (Port 8080)
echo "Starting Imperial Gateway (Port 8080)..."
nohup python3 imperial_proxy_8080.py > logs/gateway.log 2>&1 &

sleep 3

echo ""
echo "✅ IMPERIAL GATEWAY ACTIVE"
echo "==========================="
echo "🌐 Unified Access: http://localhost:8080"
echo "   • Frontend: http://localhost:8088"
echo "   • API:      http://localhost:8000"
echo "   • Dashboard: http://localhost:8092"
echo ""
echo "👑 CEO: Humbulani Mudau"
