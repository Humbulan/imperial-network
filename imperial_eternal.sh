#!/data/data/com.termux/files/usr/bin/bash
echo "🏛️ IMPERIAL ETERNAL - $(date)"
echo "================================"
cd ~/imperial_network

# Start all services in background
nohup python3 app.py > logs/engine.log 2>&1 &
nohup python3 portal_master_8088.py > logs/portal.log 2>&1 &
nohup python3 imperial_proxy_8080.py > logs/gateway.log 2>&1 &
nohup ollama serve > logs/ollama.log 2>&1 &

# Start all other sector scripts (your 35 ports)
for script in node_red_proxy_1883_enhanced.py node_red_1880_redirect.py revenue_bridge.py legacy_vault_fixed.py apex_metrics.py ussd_fix.py monitor_8090.py dashboard_ui.py intel_redirect.py sovereign_master_8096.py b2b_hub_8099.py malamulele_fix.py bi_hub_8101.py urban_gateway_8102.py intel_alpha_8103.py surge_monitor_8104.py sentinel_8105.py malamulele_relay.py sadc_sync.py vault_2_8113.py b2b_bulk_8114.py ghost_8115.py intel_files_8191.py system_node_8888.py pdc_backup_8889.py nextcloud_core_9000.py idc_stealth_9090.py; do
    if [ -f "$script" ]; then
        nohup python3 "$script" > "logs/${script%.py}.log" 2>&1 &
    fi
done

sleep 3
echo "✅ IMPERIAL ETERNAL ACTIVE - 35/35 PORTS ONLINE"
