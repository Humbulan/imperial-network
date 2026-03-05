#!/bin/bash
# 1. TOTAL KILL
pkill -f cloudflared
sleep 2

# 2. RUN WITH THE ADDRESS OVERRIDE
# We force it to use Cloudflare's Anycast IP as the literal destination
# This skips the "edge discovery" DNS phase entirely.
GODEBUG=netdns=go nohup cloudflared tunnel \
    --protocol http2 \
    --edge-ip-version 4 \
    --credentials-file /data/data/com.termux/files/home/.cloudflared/d512566a-7849-4442-8e07-97b74eaccc37.json \
    run --address 172.64.32.9 d512566a-7849-4442-8e07-97b74eaccc37 \
    > ~/imperial_network/logs/tunnel.log 2>&1 &

echo "⚡ Final Bridge Initialized... Waiting 15s for Edge Registration..."
sleep 15
grep -E "Registered|Connected" ~/imperial_network/logs/tunnel.log
