#!/bin/bash
echo "🔓 IMPERIAL TUNNEL WAKE UP COMMAND"
export GODEBUG=netdns=go
pkill -f cloudflared
sleep 2
nohup cloudflared tunnel --config /data/data/com.termux/files/home/.cloudflared/config.yml run \
  --edge-ip-version 4 \
  --protocol http2 > /data/data/com.termux/files/home/imperial_network/logs/tunnel.log 2>&1 &
sleep 5
echo "✅ TUNNEL ACTIVATED"
echo "Check with: grep \"Registered\" ~/imperial_network/logs/tunnel.log"
