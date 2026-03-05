#!/bin/bash
# 🌅 IMPERIAL MORNING ROUTINE - 06:00 AM

cd ~/imperial_network

# 1. Run industrial bridge
echo "$(date): Running Industrial Bridge" >> logs/morning.log
python3 industrial_bridge.py >> logs/morning.log 2>&1

# 2. Run village sync
echo "$(date): Running Village Sync" >> logs/morning.log
python3 sadc_village_sync_scaled.py >> logs/morning.log 2>&1

# 3. Update milestone
echo "$(date): Running Milestone Alert" >> logs/morning.log
python3 milestone_alert.py >> logs/morning.log 2>&1

# 4. Update Family Vault
echo "$(date): Updating Family Vault" >> logs/morning.log
python3 family_vault_updater.py >> logs/morning.log 2>&1

# 5. Copy latest withdrawal slip
cp ~/imperial_vault/withdrawal_*.txt /sdcard/Download/Imperial_Family_Vault/Withdrawal_Slips/ 2>/dev/null

echo "$(date): Morning routine complete" >> logs/morning.log

# 📅 TENDER COUNTDOWN - Bid 24/2025/2026
echo "$(date): Checking tender deadlines" >> logs/tender.log
target="2026-04-08"
now=$(date +%s)
target_sec=$(date -d "$target" +%s)
days=$(( ($target_sec - $now) / 86400 ))

if [ $days -le 7 ]; then
    echo "🚨 URGENT: Bid 24/2025/2026 closes in $days days!" >> logs/tender.log
    # Send SMS alert for urgent tenders
    curl -s -X POST http://localhost:8087/api/send_sms \
        -H "Content-Type: application/json" \
        -d "{\"phone\":\"0794658481\",\"message\":\"🚨 TENDER ALERT: Bid 24/2025/2026 closes in $days days! Collect documents from Office No. 02\"}" \
        > /dev/null 2>&1
else
    echo "📅 Bid 24/2025/2026 closes in $days days" >> logs/tender.log
fi
