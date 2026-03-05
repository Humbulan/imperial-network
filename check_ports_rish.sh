#!/data/data/com.termux/files/usr/bin/bash

echo "🔍 IMPERIAL PORT VERIFICATION (via rish)"
echo "=========================================="

# Ports to check
PORTS="1880 1883 8000 8001 8080 8081 8082 8083 8085 8086 8087 8088 8090 8092 8094 8095 8096 8099 8100 8101 8102 8103 8104 8105 8110 8111 8112 8113 8114 8115 8191 8888 8889 9000 9090 11434"

ONLINE=0
TOTAL=0

for PORT in $PORTS; do
    TOTAL=$((TOTAL + 1))
    RESULT=$(echo "netstat -tuln | grep :$PORT" | ./rish)
    if [ -n "$RESULT" ]; then
        echo "✅ PORT $PORT: ONLINE"
        ONLINE=$((ONLINE + 1))
    else
        echo "❌ PORT $PORT: OFFLINE"
    fi
done

echo "=========================================="
echo "📊 TOTAL: $ONLINE/$TOTAL PORTS ONLINE"
