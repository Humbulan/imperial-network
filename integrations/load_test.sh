#!/bin/bash
# Simulate enough rail traffic to hit 8.5 Gauteng score
# Each ton = progress toward the target

echo "🚂 Generating rail traffic to hit 8.5 Gauteng score..."
echo "===================================================="

TERMINALS=("city_deep" "midrand" "kaalfontein")
COMMODITIES=("87" "2616" "84" "10" "08")

for i in {1..20}; do
    TERMINAL=${TERMINALS[$RANDOM % ${#TERMINALS[@]}]}
    COMMODITY=${COMMODITIES[$RANDOM % ${#COMMODITIES[@]}]}
    TONNAGE=$((500 + RANDOM % 2000))
    
    echo -n "Sending manifest $i: $TERMINAL, $TONNAGE tons"
    
    RESPONSE=$(curl -s -X POST http://127.0.0.1:8117/api/webhooks/rail-manifest \
        -H "Content-Type: application/json" \
        -d "{
            \"manifest\": {
                \"manifest_id\": \"TEST-2026-$(printf "%03d" $i)\",
                \"train_id\": \"GAUTENG-EC-$i\",
                \"origin_terminal\": \"$TERMINAL\",
                \"destination_port\": \"ngqura\",
                \"commodity_code\": \"$COMMODITY\",
                \"gross_tonnage\": $TONNAGE,
                \"departure_time\": \"$(date -Iseconds)\",
                \"eta\": \"$(date -Iseconds -d "+2 days")\",
                \"customs_status\": \"released\"
            }
        }")
    
    SCORE=$(echo $RESPONSE | grep -o '"gauteng_score":[0-9.]*' | cut -d':' -f2)
    echo " → Score: $SCORE"
    
    # Small delay to avoid overwhelming
    sleep 0.5
done

echo ""
echo "✅ Load test complete"
echo "📊 Check final score: curl http://127.0.0.1:8117/api/metrics"
