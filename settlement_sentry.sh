#!/data/data/com.termux/files/usr/bin/bash

echo "👁️  SETTLEMENT SENTRY - Monitoring Port 8082 for confirmation"
echo "==================================================="
echo "Started: $(date)"
echo ""

while true; do
    # Check for settlement confirmation in logs
    if tail -n 5 logs/vault_confirmations.log 2>/dev/null | grep -q "SETTLEMENT CONFIRMED"; then
        echo "🔔 $(date): ✅ SETTLEMENT CONFIRMED - Funds deposited!"
        termux-vibrate -d 2000
        termux-notification --title "💰 IMPERIAL SETTLEMENT" \
                           --content "R879,441.26 has been deposited to Capitec" \
                           --priority high
        break
    fi
    
    # Check every 30 seconds
    sleep 30
done
