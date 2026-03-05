#!/bin/bash
echo "🌙 IMPERIAL NIGHTLY SYNC - $(date)"

# Source directory
BACKUP_DIR=~/imperial_network
FILES_PORT_DIR=~/imperial_network/files-browser

# Create files-browser directory if it doesn't exist
mkdir -p $FILES_PORT_DIR/backups

# Find latest backup
LATEST_BACKUP=$(ls -t $BACKUP_DIR/imperial_omega_full_state_*.tar.gz 2>/dev/null | head -1)

if [ -n "$LATEST_BACKUP" ]; then
    echo "📦 Syncing: $(basename $LATEST_BACKUP)"
    cp $LATEST_BACKUP $FILES_PORT_DIR/backups/
    
    # Also sync SADC manifest and critical configs
    cp $BACKUP_DIR/sadc_trade_manifest_*.json $FILES_PORT_DIR/backups/ 2>/dev/null
    cp $BACKUP_DIR/vouchers.json $FILES_PORT_DIR/backups/
    cp $BACKUP_DIR/.cloudflared/config.yml $FILES_PORT_DIR/backups/ 2>/dev/null
    
    # Create index
    ls -la $FILES_PORT_DIR/backups/ > $FILES_PORT_DIR/backups/backup_manifest.txt
    
    echo "✅ Sync complete - $(ls $FILES_PORT_DIR/backups/*.tar.gz | wc -l) backups available"
    echo "📱 Access via: https://files.humbu.store/backups/"
else
    echo "⚠️ No backup found to sync"
fi
