#!/data/data/com.termux/files/usr/bin/bash
cd ~/imperial_network
echo "$(date) - Running Alpha Promotion" >> logs/alpha_promotion.log
python3 -c "
import promote_data
import sqlite3
from datetime import datetime

print('🏛️ AUTO-ALPHA PROMOTION')
print('='*40)

# Check pending transactions
conn = sqlite3.connect('instance/imperial.db')
cursor = conn.cursor()
cursor.execute(\"SELECT COUNT(*) FROM nexus_backup_transaction_logs WHERE status != 'promoted' OR status IS NULL\")
pending = cursor.fetchone()[0]
conn.close()

print(f'📦 Pending in loading dock: {pending}')

if pending > 0:
    promote_data.promote_transactions()
    print('✅ Promotion complete')
else:
    print('⏭️  No pending transactions')
" >> logs/alpha_promotion.log 2>&1
