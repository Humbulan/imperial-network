#!/bin/bash
# 🏛️ IMPERIAL NETWORK - PDC TUNNEL INTEGRATION

cd ~/imperial_network

# Configuration
PDC_BIN="./pdc-agent/pdc"
TOKEN_FILE="./secrets/pdc_token.txt"
LOG_FILE="./logs/pdc_tunnel.log"
PID_FILE="./pdc-agent/pdc.pid"

# Create logs directory if needed
mkdir -p ./logs

# Check if PDC binary exists
if [ ! -f "$PDC_BIN" ]; then
    echo "❌ PDC binary not found at $PDC_BIN"
    echo ""
    echo "🔍 Please locate the pdc binary in your old project:"
    echo "   find ~/humbu_community_nexus -name 'pdc' -type f"
    echo ""
    echo "Then copy it to: $PDC_BIN"
    exit 1
fi

# Check if token exists
if [ ! -f "$TOKEN_FILE" ]; then
    echo "❌ PDC token not found at $TOKEN_FILE"
    exit 1
fi

TOKEN=$(cat "$TOKEN_FILE")

# Check if already running
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "⚠️ PDC tunnel already running with PID: $OLD_PID"
        echo "   Stop it first with: ./stop_pdc_tunnel.sh"
        exit 1
    fi
fi

echo "🏛️ IMPERIAL PDC TUNNEL - STARTING"
echo "========================================"
echo "📅 $(date)"
echo ""
echo "🔌 Tunneling Imperial Network ports:"
echo "   • 8102 - Urban Gateway"
echo "   • 8000 - Business API"
echo "   • 8099 - B2B Hub"
echo "   • 8082 - Revenue Bridge (Imperial Alpha)"
echo "   • 8093 - System Stats"
echo ""

# Start the tunnel
nohup sh -c "SSL_CERT_FILE=$PREFIX/etc/tls/cert.pem termux-chroot $PDC_BIN \
  -token $TOKEN \
  -cluster prod-eu-west-2 \
  -gcloud-hosted-grafana-id 1220124 \
  -metrics-addr :8091 \
  -ssh-flag '-oPermitRemoteOpen=localhost:8102' \
  -ssh-flag '-oPermitRemoteOpen=localhost:8000' \
  -ssh-flag '-oPermitRemoteOpen=localhost:8099' \
  -ssh-flag '-oPermitRemoteOpen=localhost:8082' \
  -ssh-flag '-oPermitRemoteOpen=localhost:8093'" > "$LOG_FILE" 2>&1 &

NEW_PID=$!
echo $NEW_PID > "$PID_FILE"

echo "🚀 PDC Tunnel started with PID: $NEW_PID"
echo "📁 Logs: $LOG_FILE"
echo ""
echo "📊 Monitor with: tail -f $LOG_FILE"
echo "🛑 Stop with: ./stop_pdc_tunnel.sh"
