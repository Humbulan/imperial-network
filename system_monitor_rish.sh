#!/data/data/com.termux/files/usr/bin/bash

echo "📱 IMPERIAL SYSTEM MONITOR (via rish)"
echo "======================================="
cd ~/imperial_network

# Function to run commands via rish
run_rish() {
    echo "$1" | ./rish
}

echo "🔋 Battery Status:"
run_rish "dumpsys battery" | grep -E "level|status|temperature|voltage"

echo -e "\n📱 Device Info:"
run_rish "getprop ro.product.manufacturer"
run_rish "getprop ro.product.model"
run_rish "getprop ro.build.version.release"

echo -e "\n💾 Storage Info:"
run_rish "df -h /data"

echo -e "\n📊 Running Services:"
run_rish "ps -A | grep -E 'python|node|ollama|filebrowser'"

echo -e "\n🌐 Network Connections:"
run_rish "netstat -tuln | grep -E ':(1880|1883|8000|8080|8090|8092|8095|8102|8112|8888|9090|11434)'"

echo -e "\n✅ System Monitor Complete"
