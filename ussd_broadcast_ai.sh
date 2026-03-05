#!/data/data/com.termux/files/usr/bin/bash

echo "📱 USSD BROADCAST - IMPERIAL COUNCIL"
echo "==================================================="
echo "Sending to Port 8087 (USSD Portal)..."
echo ""

# Broadcast message for top 10 referrers
curl -X POST http://localhost:8087/api/broadcast \
  -H "Content-Type: application/json" \
  -d '{
    "recipients": "top_10_referrers",
    "priority": "HIGH",
    "message": "🏆 IMPERIAL REWARD: Microsoft AI Beta Vouchers\n\nYou have been selected for exclusive access to Microsoft'\''s 2026 AI certifications (AI-103, AB-730). These beta vouchers represent global accreditation for your sovereign skills.\n\nReply with ACCEPT to claim your voucher code.\n\nVoucher value: R15,000+ each\nExpires: 2026-06-30\n\n👑 CEO: Humbulani Mudau",
    "type": "CERTIFICATION_REWARD",
    "source": "Microsoft AI Partnership"
  }'

echo ""
echo "✅ Broadcast dispatched to USSD Gateway"
echo "📊 Check responses: tail -f logs/ussd_responses.log"
echo "==================================================="
