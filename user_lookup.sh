#!/data/data/com.termux/files/usr/bin/bash
# Quick user lookup by phone or username

if [ -z "$1" ]; then
    echo "Usage: ./user_lookup.sh <phone or username>"
    exit 1
fi

cd ~/imperial_network
sqlite3 instance/imperial.db "SELECT id, username, phone, village, role, created_at FROM user WHERE phone LIKE '%$1%' OR username LIKE '%$1%' OR village LIKE '%$1%';"
