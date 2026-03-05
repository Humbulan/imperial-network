#!/data/data/com.termux/files/usr/bin/bash

# MTN Ghana Position - March 2026
SHARES=883321
DIVIDEND_CASH=353328.40
MTN_PRICE=5.78
EX_DIV_DATE="2026-03-24"
PAYMENT_DATE="2026-04-10"

# Scrip calculation (shares instead of cash)
SCRIP_SHARES=$(echo "$DIVIDEND_CASH / $MTN_PRICE" | bc)
TOTAL_AFTER_SCRIP=$(echo "$SHARES + $SCRIP_SHARES" | bc)
FUTURE_DIVIDEND=$(echo "$TOTAL_AFTER_SCRIP * 0.40" | bc)

echo ""
echo "📈 MTN GHANA DIVIDEND POSITION - MARCH 2026"
echo "-------------------------------------------------------"
echo "   • Shares Acquired:     $(printf "%'d" $SHARES)"
echo "   • Projected Dividend:  GH₵ $(printf "%'.2f" $DIVIDEND_CASH)"
echo "   • Ex-Dividend Date:    $EX_DIV_DATE"
echo "   • Payment Date:        $PAYMENT_DATE"
echo "   • Status:              🟢 SECURED"
echo ""
echo "🔄 SCRIP DIVIDEND OPTION (Shares instead of Cash)"
echo "   • New shares if scrip: $(printf "%'d" $SCRIP_SHARES)"
echo "   • Total after scrip:   $(printf "%'d" $TOTAL_AFTER_SCRIP)"
echo "   • 2027 Dividend:       GH₵ $(printf "%'.2f" $FUTURE_DIVIDEND)"
echo "   • Annual Growth:       +$(echo "scale=2; $SCRIP_SHARES * 100 / $SHARES" | bc)%"
echo "-------------------------------------------------------"
