#!/bin/bash
# 🔍 Imperial Network Service Checker

echo "🏛️ IMPERIAL NETWORK - SERVICE STATUS"
echo "==================================="

check_port() {
    local port=$1
    local service=$2
    if lsof -i :$port > /dev/null 2>&1; then
        echo "✅ $service (port $port): ACTIVE"
        # Get PID of the service
        PID=$(lsof -t -i:$port 2>/dev/null | head -1)
        if [ ! -z "$PID" ]; then
            echo "   └─ PID: $PID"
        fi
    else
        echo "❌ $service (port $port): INACTIVE"
    fi
}

echo ""
check_port 8102 "Urban Gateway"
check_port 8000 "Business API"
check_port 8099 "B2B Hub"
check_port 8082 "Revenue Bridge"
check_port 8093 "System Stats"
echo ""
echo "📁 Logs directory: ~/imperial_network/logs/"
echo "💡 To start services, check migrated/ directories"
