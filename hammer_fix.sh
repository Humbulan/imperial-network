#!/bin/bash
# 1. KILL ALL HANGING PROCESSES
pkill -f cloudflared
sleep 2

# 2. FORCE THE IP BINDING
# We use the --address flag with the SPECIFIC Cloudflare Edge IP
# This tells the binary: "Do not look for the edge, I found it for you."
export GODEBUG=netdns=go
nohup cloudflared tunnel \
    --edge-ip-version 4 \
    --protocol http2 \
    --credentials-file /data/data/com.termux/files/home/.cloudflared/d512566a-7849-4442-8e07-97b74eaccc37.json \
    run --address 172.64.32.9 d512566a-7849-4442-8e07-97b74eaccc37 \
    > ~/imperial_network/logs/tunnel.log 2>&1 &

echo "🔨 Hammer Drop Initialized. Checking for registration..."
sleep 15
grep -E "Registered|Connected" ~/imperial_network/logs/tunnel.log || tail -n 10 ~/imperial_network/logs/tunnel.log
