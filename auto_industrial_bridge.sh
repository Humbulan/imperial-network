#!/bin/bash
# 🏭 Auto Industrial Bridge - Runs daily at 06:00

cd ~/imperial_network
echo "$(date): Running Industrial Bridge" >> logs/industrial_bridge.log
python3 industrial_bridge.py >> logs/industrial_bridge.log 2>&1
