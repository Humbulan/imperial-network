#!/bin/bash
# 🌅 Daily Milestone Alert - Runs at 6:00 AM

cd ~/imperial_network
echo "$(date): Running Daily Milestone Alert" >> logs/milestone.log
python3 milestone_alert.py >> logs/milestone.log 2>&1

# Also append to family dividends
python3 milestone_alert.py >> ~/imperial_vault/family_dividends.log 2>&1
