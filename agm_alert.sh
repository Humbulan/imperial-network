#!/data/data/com.termux/files/usr/bin/bash

# AGM Reminder for March 24, 2026
echo "========================================="
echo "📅 MTN GHANA AGM REMINDER - MARCH 24, 2026"
echo "========================================="
echo ""

# Check current position
SHARES=883321
DIVIDEND=353328.40
PRICE=5.78

echo "📊 CURRENT POSITION:"
echo "   • Shares: $(printf "%'d" $SHARES)"
echo "   • Dividend Due: GH₵ $(printf "%'.2f" $DIVIDEND)"
echo "   • Ex-Dividend Date: TODAY (March 24)"
echo ""

echo "⚡ ACTION REQUIRED - SCRIP ELECTION:"
echo "   1. Log into Central Securities Depository (CSD)"
echo "   2. Navigate to MTN Ghana (SCANCOM PLC)"
echo "   3. Select 'Scrip Dividend Election'"
echo "   4. Choose 100% SHARES instead of cash"
echo ""

SCRIP_SHARES=$(echo "$DIVIDEND / $PRICE" | bc)
TOTAL_AFTER=$(echo "$SHARES + $SCRIP_SHARES" | bc)

echo "🎯 IF YOU SCRIP TODAY:"
echo "   • New shares acquired: $(printf "%'d" $SCRIP_SHARES)"
echo "   • Total holdings by April 10: $(printf "%'d" $TOTAL_AFTER)"
echo "   • 2027 dividend projection: GH₵ $(printf "%'.2f" $(echo "$TOTAL_AFTER * 0.40" | bc))"
echo ""
echo "========================================="
