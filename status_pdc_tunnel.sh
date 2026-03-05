#!/bin/bash
# 📊 Check PDC Tunnel Status

PID_FILE="./pdc-agent/pdc.pid"

echo "🏛️ IMPERIAL PDC TUNNEL STATUS"
echo "========================================"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "✅ PDC tunnel RUNNING (PID: $PID)"
        echo ""
        echo "📊 Process details:"
        ps -f -p "$PID"
        echo ""
        echo "📁 Last 5 log entries:"
        tail -5 ./logs/pdc_tunnel.log 2>/dev/null || echo "No logs yet"
    else
        echo "⚠️ PDC tunnel NOT RUNNING (stale PID file)"
        rm "$PID_FILE"
    fi
else
    # Check by process name
    PIDS=$(pgrep -f "pdc.*-token")
    if [ ! -z "$PIDS" ]; then
        echo "⚠️ PDC tunnel running but no PID file:"
        ps -f -p $PIDS
    else
        echo "❌ PDC tunnel NOT RUNNING"
    fi
fi
