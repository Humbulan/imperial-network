#!/data/data/com.termux/files/usr/bin/bash

echo ""
echo "📈 APRIL REBASE PREVIEW (Post-Scrip Election)"
echo "========================================"

# Current position
SHARES=883321
DIVIDEND=353328.40
PRICE=5.78
EXCHANGE_RATE=0.45

# Scrip calculation
SCRIP_SHARES=$(echo "$DIVIDEND / $PRICE" | bc)
TOTAL_SHARES=$(echo "$SHARES + $SCRIP_SHARES" | bc)
NEW_DIVIDEND=$(echo "$TOTAL_SHARES * 0.40" | bc)
MTN_VALUE_RAND=$(echo "$TOTAL_SHARES * $PRICE * $EXCHANGE_RATE" | bc)

echo "📊 MTN GHANA POSITION (Post-April 10)"
echo "   • Current shares:      $(printf "%'d" $SHARES)"
echo "   • Scrip shares added:  $(printf "%'d" $SCRIP_SHARES)"
echo "   • Total shares:        $(printf "%'d" $TOTAL_SHARES)"
echo "   • Value (Rands):       R$(printf "%'.2f" $MTN_VALUE_RAND)"
echo "   • 2027 dividend:       GH₵ $(printf "%'.2f" $NEW_DIVIDEND)"
echo ""

# Wealth Lock impact
CURRENT_WEALTH_LOCK=238050000.00
NEW_WEALTH_LOCK=$(echo "$CURRENT_WEALTH_LOCK + $MTN_VALUE_RAND" | bc)

echo "💰 WEALTH LOCK PROJECTION"
echo "   • Current gain:        R$(printf "%'.2f" $CURRENT_WEALTH_LOCK)"
echo "   • MTN contribution:    R$(printf "%'.2f" $MTN_VALUE_RAND)"
echo "   • Post-rebase gain:    R$(printf "%'.2f" $NEW_WEALTH_LOCK)"
echo "   • True valuation:      R$(printf "%'.2f" $(echo "1568116092.14 + $NEW_WEALTH_LOCK" | bc))"
echo "========================================"
