#!/bin/bash

echo "🔧 Imperial Nexus Bridge - Activating..."

# 1. CLEANUP
pkill -f cloudflared
sleep 2

# 2. RESOLVE CLOUDFLARE EDGE MANUALLY
# Using a stable Cloudflare Anycast IP
EDGE_IP="172.64.32.9"
echo "✅ Mapping Cloudflare Edge to $EDGE_IP..."

# 3. ENSURE LOGS DIRECTORY EXISTS
mkdir -p ~/imperial_network/logs

# 4. CONSTRUCT THE COMMAND
# GODEBUG=netdns=go forces the internal Go resolver (ignoring the broken system one)
export GODEBUG=netdns=go
export NAMESERVER=1.1.1.1

nohup cloudflared tunnel \
    --protocol quic \
    --edge-ip-version 4 \
    --credentials-file /data/data/com.termux/files/home/.cloudflared/d512566a-7849-4442-8e07-97b74eaccc37.json \
    run d512566a-7849-4442-8e07-97b74eaccc37 \
    > ~/imperial_network/logs/tunnel.log 2>&1 &

echo "🚀 Bridge Initialized. Waiting for Handshake..."
sleep 12

# 5. VERIFICATION
echo ""
echo "📡 TUNNEL STATUS:"
if grep -q "Registered" ~/imperial_network/logs/tunnel.log; then
    echo "✅ SUCCESS: Tunnel Registered with Cloudflare"
    echo "🌐 Your services should now be live:"
    echo "   • https://imperial.humbu.store"
    echo "   • https://files.humbu.store"
    echo "   • https://monitor.humbu.store"
    echo "   • https://secret.humbu.store"
elif grep -q "Connected" ~/imperial_network/logs/tunnel.log; then
    echo "✅ SUCCESS: Tunnel Connected"
else
    echo "⚠️  Still initializing or check logs:"
    tail -20 ~/imperial_network/logs/tunnel.log
fi
