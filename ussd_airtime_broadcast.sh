#!/data/data/com.termux/files/usr/bin/bash

echo "📱 IMPERIAL AIRTIME - REAL VALUE ANNOUNCEMENT"
echo "==================================================="

curl -X POST http://localhost:8087/api/broadcast \
  -H "Content-Type: application/json" \
  -d '{
    "recipients": "all_sovereigns",
    "priority": "HIGH",
    "message": "💰 IMPERIAL KEINS NOW REDEEMABLE FOR REAL AIRTIME!\n\nYour AI access keys (0YUH-XKME, etc.) can now be redeemed for actual Vodacom/MTN airtime.\n\nTo redeem:\n1. Dial *120*IMPERIAL# on your phone\n2. Enter your voucher key\n3. Enter your cell number\n4. Get instant airtime!\n\nR50, R100, R25 denominations available.\n\nFirst 100 redemptions get DOUBLE value!\n\n👑 CEO: Humbulani Mudau",
    "type": "VAS_LAUNCH",
    "expiry": "2026-06-30"
  }'

echo ""
echo "✅ Airtime redemption broadcast sent"
echo "📊 Monitor: tail -f logs/vas_bridge.log"
echo "==================================================="
