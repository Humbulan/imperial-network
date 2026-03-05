#!/data/data/com.termux/files/usr/bin/bash

echo "📥 Importing Temperature Monitor Flow to Node-RED..."

# Check if Node-RED is running
if ! curl -s http://localhost:1880 > /dev/null; then
    echo "❌ Node-RED is not running on port 1880"
    echo "Starting Node-RED..."
    node-red -p 1880 &
    sleep 5
fi

# Use Node-RED admin API to import flow
# Note: This requires Node-RED admin API to be enabled
# For now, we'll provide instructions for manual import
echo ""
echo "📋 MANUAL IMPORT INSTRUCTIONS:"
echo "================================"
echo "1. Open Node-RED in your browser: http://localhost:1880"
echo "2. Click the menu (☰) in the top-right corner"
echo "3. Select 'Import'"
echo "4. Copy and paste the contents of this file:"
echo "   ~/imperial_network/temperature_monitor_flow.json"
echo "5. Click 'Import'"
echo "6. Click 'Deploy' in the top-right corner"
echo ""
echo "📁 Flow file location: ~/imperial_network/temperature_monitor_flow.json"
