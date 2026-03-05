#!/data/data/com.termux/files/usr/bin/bash
cd ~/imperial_network
python3 sadc_trade_intel.py --update >> ~/logs/trade_updates.log 2>&1
echo "Trade data updated: $(date)" >> ~/logs/trade_cron.log
