#!/bin/bash
# 1. KILL ALL GHOSTS
pkill -f cloudflared
sleep 1

# 2. THE DNS BYPASS (HARDCODE THE EDGE)
# We map the discovery endpoint to a verified Cloudflare IPv4 Edge IP
echo "172.64.32.9 _v2-origintunneld._tcp.argotunnel.com" > ~/hosts_override
echo "172.64.32.9 argotunnel.com" >> ~/hosts_override

# 3. ACTIVATE TUNNEL WITH STATIC DISCOVERY
# We use --protocol http2 because it's more stable when forcing IPs in Termux
export GODEBUG=netdns=go
nohup cloudflared tunnel \
    --protocol http2 \
    --edge-ip-version 4 \
    --credentials-file /data/data/com.termux/files/home/.cloudflared/d512566a-7849-4442-8e07-97b74eaccc37.json \
    run d512566a-7849-4442-8e07-97b74eaccc37 \
    > ~/imperial_network/logs/tunnel.log 2>&1 &

echo "🚀 Sovereign Bridge Activated. Verifying handshake..."
sleep 12
grep -E "Registered|Connected" ~/imperial_network/logs/tunnel.log
