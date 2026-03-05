#!/bin/bash
# 🔍 Imperial Website Diagnostic Tool

echo "🏛️ IMPERIAL WEBSITE DIAGNOSTIC"
echo "=============================="

# Check if server is running
if lsof -i :8088 > /dev/null 2>&1; then
    echo "✅ Server is running on port 8088"
    SERVER_PID=$(lsof -t -i:8088)
    echo "   PID: $SERVER_PID"
else
    echo "❌ Server is NOT running on port 8088"
fi

# Check endpoints
echo -e "\n📋 ENDPOINT STATUS:"
for endpoint in "/" "/main" "/front.html" "/index.html.original"; do
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8088$endpoint)
    if [ "$STATUS" = "200" ]; then
        echo "   ✅ $endpoint - OK (200)"
    elif [ "$STATUS" = "404" ]; then
        echo "   ❌ $endpoint - Not Found (404)"
    else
        echo "   ⚠️ $endpoint - Status: $STATUS"
    fi
done

# Show last 10 log entries
echo -e "\n📋 LAST 10 LOG ENTRIES:"
tail -10 ~/imperial_network/logs/website.log 2>/dev/null || echo "No logs found"

echo -e "\n📁 Website directory: $(lsof -p $SERVER_PID 2>/dev/null | grep cwd | awk '{print $9}')"
