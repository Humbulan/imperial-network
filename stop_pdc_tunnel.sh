#!/bin/bash
# 🛑 Stop PDC Tunnel

PID_FILE="./pdc-agent/pdc.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "🛑 Stopping PDC tunnel (PID: $PID)..."
        kill "$PID"
        rm "$PID_FILE"
        echo "✅ PDC tunnel stopped"
    else
        echo "⚠️ No PDC tunnel running (stale PID file)"
        rm "$PID_FILE"
    fi
else
    # Try to find by process name
    PIDS=$(pgrep -f "pdc.*-token")
    if [ ! -z "$PIDS" ]; then
        echo "🛑 Stopping PDC processes: $PIDS"
        pkill -f "pdc.*-token"
        echo "✅ PDC tunnel stopped"
    else
        echo "✅ No PDC tunnel running"
    fi
fi
