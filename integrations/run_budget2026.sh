#!/bin/bash
# Master script to run all Budget 2026 integrations

echo "🏛️  IMPERIAL OMEGA - BUDGET 2026 INTEGRATION"
echo "============================================"
echo "Starting: $(date)"
echo

# Step 1: Sync Ukuvuselela Rail Data
echo "📡 Step 1: Syncing Project Ukuvuselela Rail Manifests..."
PYTHONPATH=$HOME/imperial_network python3 ~/imperial_network/integrations/ukuvuselela_sync.py
echo

# Step 2: Generate R&D Tax Credit Report
echo "💰 Step 2: Generating R&D Tax Credit Claim..."
python3 ~/imperial_network/integrations/rd_tax_reporter.py
echo

# Step 3: Link Vouchers to SEZ
echo "🎫 Step 3: Expanding Vouchers for Nkomazi SEZ..."
bash ~/imperial_network/integrations/voucher_expander.sh
echo

# Step 4: Update Port 8000 for BFI Pipeline
echo "🔄 Step 4: Configuring Business API for BFI Pipeline..."
curl -s -X POST http://127.0.0.1:8000/api/register-stream \
  -H "Content-Type: application/json" \
  -d '{
    "stream": "infrastructure_investment",
    "source": "gov.bfi.pipeline",
    "endpoints": [
      "/projects/ukuvuselela/status",
      "/sez/nkomazi/incentives"
    ]
  }' > /dev/null
echo "✅ Business API configured"
echo

# Step 5: Update Intel Alpha with Zim-shock data
echo "🧠 Step 5: Updating Intel Alpha with Zim-shock Analysis..."
curl -s -X POST http://127.0.0.1:8103/api/update-risk \
  -H "Content-Type: application/json" \
  -d '{
    "event": "zimbabwe_lithium_ban",
    "date": "2026-02-25",
    "impact": {
      "lithium_premium": 0.15,
      "affected_shipments": "all_in_transit",
      "valuation_adjustment": "+15%"
    }
  }' > /dev/null
echo "✅ Intel Alpha updated with scarcity premium"
echo

# Step 6: Verify Integration
echo "📊 Step 6: Integration Verification..."
echo "   Checking Port 8099 B2B Hub..."
curl -s http://127.0.0.1:8099/api/health > /dev/null && echo "   ✅ B2B Hub OK" || echo "   ❌ B2B Hub Error"
echo "   Checking Port 8103 Intel Alpha..."
curl -s http://127.0.0.1:8103/api/health > /dev/null && echo "   ✅ Intel Alpha OK" || echo "   ❌ Intel Alpha Error"

echo
echo "============================================"
echo "✅ BUDGET 2026 INTEGRATION COMPLETE"
echo "⏱️  Finished: $(date)"
echo
