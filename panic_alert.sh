#!/data/data/com.termux/files/usr/bin/bash

OFFLINE_PORTS=()
echo "🔍 Checking all 48 ports..."

for port in 1880 1883 8000 8001 8080 8081 8082 8083 8085 8086 8087 8088 8090 8091 8092 8093 8094 8095 8096 8097 8098 8099 8100 8101 8102 8103 8104 8105 8106 8107 8108 8110 8111 8112 8113 8114 8115 8117 8191 8880 8888 8889 9000 9001 9002 9003 9090 11434; do
    if ! curl -s -I http://localhost:$port --connect-timeout 2 > /dev/null 2>&1; then
        OFFLINE_PORTS+=($port)
        echo "🔴 OFFLINE: Port $port"
    fi
done

if [ ${#OFFLINE_PORTS[@]} -gt 0 ]; then
    echo "🚨 IMPERIAL PANIC - PORTS OFFLINE" > ~/imperial_network/tmp/panic_email.txt
    echo "Offline ports: ${OFFLINE_PORTS[*]}" >> ~/imperial_network/tmp/panic_email.txt
    echo "Timestamp: $(date)" >> ~/imperial_network/tmp/panic_email.txt
    echo "📧 Alert saved to ~/imperial_network/tmp/panic_email.txt"
    
    # Send email (configure your email here)
    # mail -s "IMPERIAL PANIC - PORTS OFFLINE" your@email.com < ~/imperial_network/tmp/panic_email.txt
else
    echo "✅ All 48 ports online"
fi
