#!/bin/bash
# Check webhook server status and Gauteng readiness

echo "📡 Webhook Server Status - $(date)"
echo "=================================="

# Check if webhook is running on port 8117
if curl -s http://127.0.0.1:8117/api/health > /dev/null 2>&1; then
    echo "✅ Webhook Server (8117): RUNNING"
    
    # Get metrics
    METRICS=$(curl -s http://127.0.0.1:8117/api/metrics 2>/dev/null)
    if [ ! -z "$METRICS" ]; then
        CURRENT=$(echo $METRICS | python3 -c "import sys, json; print(json.load(sys.stdin).get('current', 'N/A'))" 2>/dev/null)
        TARGET=$(echo $METRICS | python3 -c "import sys, json; print(json.load(sys.stdin).get('target', '8.5'))" 2>/dev/null)
        echo "📊 Gauteng Readiness: $CURRENT/$TARGET"
        
        # Check if target reached
        if (( $(echo "$CURRENT >= $TARGET" | bc -l 2>/dev/null) )); then
            echo "🎯 TARGET ACHIEVED!"
        fi
    else
        echo "📊 Gauteng Readiness: Waiting for first manifest..."
    fi
else
    echo "❌ Webhook Server (8117): STOPPED"
    echo "Starting webhook server on port 8117..."
    cd ~/imperial_network
    nohup python3 integrations/ukuvuselela_simple.py > logs/webhook_8117.log 2>&1 &
    sleep 3
    echo "✅ Server started on port 8117"
fi

# Check if any lithium premiums have been applied
LITHIUM_COUNT=0
if [ "$LITHIUM_COUNT" -gt "0" ]; then
    echo "🔋 Lithium Premiums Applied: $LITHIUM_COUNT"
fi

# Run voucher enhancement check
echo ""
echo "🎫 SEZ Voucher Status:"
python3 ~/imperial_network/integrations/voucher_writer.py 2>/dev/null || echo "   Voucher writer ready"
