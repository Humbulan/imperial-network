#!/bin/bash
# 🔍 PDC Diagnostic Tool

echo "🏛️ PDC DIAGNOSTIC REPORT"
echo "========================"

echo -e "\n📁 Binary location:"
ls -la ~/imperial_network/pdc-agent/pdc 2>/dev/null || echo "   ❌ Binary missing"

echo -e "\n🔑 Token file:"
ls -la ~/imperial_network/secrets/pdc_token.txt 2>/dev/null || echo "   ❌ Token missing"
if [ -f ~/imperial_network/secrets/pdc_token.txt ]; then
    echo "   Token length: $(wc -c < ~/imperial_network/secrets/pdc_token.txt) bytes"
fi

echo -e "\n📊 Running processes:"
pgrep -fl pdc || echo "   No PDC processes running"

echo -e "\n📁 Log files:"
ls -la ~/imperial_network/logs/pdc_tunnel.log 2>/dev/null || echo "   ❌ Log file missing"
if [ -f ~/imperial_network/logs/pdc_tunnel.log ]; then
    echo -e "\n📋 Last 10 log entries:"
    tail -10 ~/imperial_network/logs/pdc_tunnel.log 2>/dev/null || echo "   Log empty"
fi

echo -e "\n🔌 Port status:"
for port in 8102 8000 8099 8082 8093; do
    if lsof -i :$port > /dev/null 2>&1; then
        echo "   ✅ Port $port is active"
    else
        echo "   ⚠️ Port $port is not active"
    fi
done

echo -e "\n✅ Diagnostic complete"
