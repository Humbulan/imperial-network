#!/data/data/com.termux/files/usr/bin/bash
# Sync legacy users from humbu_community_nexus to imperial_network

LEGACY_VAULT=~/humbu_community_nexus/Imperial_Omega/LEGACY_708_VAULT/OFFICIAL_RECORDS/MASTER_USER_DIRECTORY.csv

if [ -f "$LEGACY_VAULT" ]; then
    echo "$(date): Syncing legacy users..." >> ~/imperial_network/logs/legacy_sync.log
    
    cd ~/imperial_network
    python3 -c "
import csv, sqlite3
from datetime import datetime

conn = sqlite3.connect('instance/imperial.db')
c = conn.cursor()

with open('$LEGACY_VAULT', 'r') as f:
    reader = csv.DictReader(f)
    synced = 0
    for row in reader:
        try:
            c.execute('''
                INSERT OR IGNORE INTO user (name, phone, village, created_at, status, migrated_from)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                row.get('name', 'Unknown'),
                row.get('phone', '').strip(),
                row.get('village', ''),
                datetime.now().isoformat(),
                'active',
                'legacy_sync'
            ))
            if c.rowcount > 0:
                synced += 1
        except:
            pass
    
    conn.commit()
    c.execute('SELECT COUNT(*) FROM user')
    total = c.fetchone()[0]
    conn.close()
    
    print(f'Synced {synced} new users. Total: {total}')
" >> ~/imperial_network/logs/legacy_sync.log 2>&1
fi
