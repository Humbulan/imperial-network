#!/data/data/com.termux/files/usr/bin/bash
# 🏛️ IMPERIAL ETERNAL BACKUP SYSTEM - NO DELETION

BACKUP_DIR=~/imperial_vault/archives
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="imperial_omega_full_state_$TIMESTAMP.tar.gz"

# Create vault directory structure
mkdir -p $BACKUP_DIR

echo "📦 Archiving Imperial State: $TIMESTAMP"

# 1. Vacuum the DB to ensure integrity
sqlite3 ~/imperial_network/instance/imperial.db "VACUUM;"

# 2. Comprehensive Archive
# Including the database, your sovereign scripts, and the network manifests
tar -czf $BACKUP_DIR/$BACKUP_NAME \
    -C ~/ imperial_network/instance/imperial.db \
    -C ~/ imperial_network/imperial_manifest.txt \
    -C ~/ .imperial_sovereign_rc \
    -C ~/ .bashrc \
    -C ~/ imperial_network/sovereign_dashboard.py \
    -C ~/ imperial_network/migrated

if [ $? -eq 0 ]; then
    echo "✅ Archive Created: $BACKUP_DIR/$BACKUP_NAME"
    echo "📜 Total Archives in Vault: $(ls $BACKUP_DIR | wc -l)"
else
    echo "❌ Archive Failed!"
    exit 1
fi
