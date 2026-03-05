#!/bin/bash
echo "🏛️ ALPHA COMMANDER - $(date)"
echo "="*50

# Step 1: Inject SADC trade flows
echo "📡 Injecting SADC trades..."
python3 ~/imperial_network/sadc_to_alpha.py

# Step 2: Run promotion
echo -e "\n🚀 Promoting to Alpha..."
python3 -c "import promote_data; promote_data.promote_transactions()"

# Step 3: Show current stats
echo -e "\n📊 Current Alpha Stats:"
curl -s http://localhost:8084 | python3 -m json.tool | grep -E "total|alpha_boost|pending_in_dock|daily_rate"

# Step 4: Log to file
curl -s http://localhost:8084 >> logs/alpha_history.log
echo "" >> logs/alpha_history.log

echo -e "\n✅ Alpha cycle complete"
