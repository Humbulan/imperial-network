#!/bin/bash
# 🏛️ IMPERIAL COOKIE HEARTBEAT & SANITIZER WITH ALERTS

TARGET="https://secret.humbu.store/login"
COOKIE="imperial_access=granted"
# Sanitizer Targets: 5173 (Vite), 8080 (Dev), 8082 (Mirrored UI), 8083 (Legacy)
CLEAN_PORTS=(5173 8080 8082 8083)
HEARTBEAT_LOG="$HOME/imperial_network/logs/heartbeat.log"
SANITIZER_LOG="$HOME/imperial_network/logs/sanitizer_alerts.log"

# Create logs directory if it doesn't exist
mkdir -p "$HOME/imperial_network/logs"

# Function to send alert to dashboard (via Node-RED or USSD)
send_alert() {
    local message="$1"
    local severity="$2"
    
    # Log to sanitizer alerts file
    echo "$(date) | [$severity] $message" >> "$SANITIZER_LOG"
    
    # Optional: Send to dashboard via Port 8086 (Apex Metrics)
    curl -s -X POST "http://localhost:8086/api/alert" \
        -H "Content-Type: application/json" \
        -d "{\"message\":\"$message\",\"severity\":\"$severity\",\"timestamp\":\"$(date -Iseconds)\"}" \
        > /dev/null 2>&1
}

echo "🏛️ IMPERIAL SANITIZER HEARTBEAT STARTED at $(date)" >> "$HEARTBEAT_LOG"
echo "Protected Ports: ${CLEAN_PORTS[*]}" >> "$HEARTBEAT_LOG"
echo "Target: $TARGET" >> "$HEARTBEAT_LOG"
echo "----------------------------------------" >> "$HEARTBEAT_LOG"

while true; do
    SANITIZER_ACTIONS=0
    
    # 1. THE SANITIZER: Kill rogue processes on restricted ports
    for PORT in "${CLEAN_PORTS[@]}"; do
        PIDS=$(lsof -t -i:"$PORT" 2>/dev/null)
        if [ ! -z "$PIDS" ]; then
            for PID in $PIDS; do
                # Get process info before killing
                PROCESS_INFO=$(ps -p $PID -o comm= 2>/dev/null || echo "unknown")
                SANITIZER_ACTIONS=$((SANITIZER_ACTIONS + 1))
                
                echo "$(date) | 🛡️ SANITIZER: Killing rogue process $PID ($PROCESS_INFO) on port $PORT" >> "$HEARTBEAT_LOG"
                kill -9 $PID > /dev/null 2>&1
                
                # Send alert for rogue process
                send_alert "Rogue process killed: $PROCESS_INFO (PID: $PID) on port $PORT" "WARNING"
            done
        fi
    done
    
    # 2. THE HEARTBEAT: Keep the Sovereign session alive
    START_TIME=$(date +%s%N)
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" -H "Cookie: $COOKIE" "$TARGET" 2>/dev/null)
    END_TIME=$(date +%s%N)
    LATENCY=$(( ($END_TIME - $START_TIME) / 1000000 )) # Convert to milliseconds
    
    if [ "$STATUS" -eq 200 ]; then
        if [ $SANITIZER_ACTIONS -gt 0 ]; then
            echo "$(date) | 🟢 Dashboard Accessible (Cookie Verified) | Sanitized: $SANITIZER_ACTIONS processes" >> "$HEARTBEAT_LOG"
        else
            echo "$(date) | 🟢 Dashboard Accessible (Cookie Verified) | Latency: ${LATENCY}ms" >> "$HEARTBEAT_LOG"
        fi
    elif [ "$STATUS" -eq 401 ] || [ "$STATUS" -eq 403 ]; then
        echo "$(date) | 🔴 Authentication Failed | Status: $STATUS | Cookie may have expired" >> "$HEARTBEAT_LOG"
        send_alert "Authentication failed with status $STATUS" "CRITICAL"
    elif [ "$STATUS" -eq 000 ]; then
        echo "$(date) | ⚫ Network Error | Cannot reach $TARGET" >> "$HEARTBEAT_LOG"
        send_alert "Network connectivity lost to dashboard" "CRITICAL"
    else
        echo "$(date) | ⚠️ Connection Issue | Status: $STATUS | Latency: ${LATENCY}ms" >> "$HEARTBEAT_LOG"
        if [ $STATUS -ge 500 ]; then
            send_alert "Server error $STATUS from dashboard" "ERROR"
        fi
    fi
    
    # Rotate logs if they get too large (keep last 1000 lines)
    if [ -f "$HEARTBEAT_LOG" ] && [ $(wc -l < "$HEARTBEAT_LOG") -gt 1000 ]; then
        tail -n 500 "$HEARTBEAT_LOG" > "$HEARTBEAT_LOG.tmp"
        mv "$HEARTBEAT_LOG.tmp" "$HEARTBEAT_LOG"
    fi
    
    sleep 30
done
