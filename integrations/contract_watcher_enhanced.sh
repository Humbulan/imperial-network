#!/bin/bash
# 📋 Enhanced Contract Watcher - Tracks both digital and physical tenders

cd ~/imperial_network

echo "📋 THULAMELA TENDER MONITOR - ENHANCED"
echo "========================================"
echo "Generated: $(date)"
echo ""

# Define tenders (both digital and physical)
declare -A TENDERS=(
    ["08/2025/2026"]="Road Rehabilitation|Digital|thulamela.gov.za"
    ["24/2025/2026"]="IT Printers (3 Year)|PHYSICAL|Office No. 02"
)

for tender in "${!TENDERS[@]}"; do
    IFS='|' read -r desc type location <<< "${TENDERS[$tender]}"
    
    echo "📄 BID $tender - $desc"
    echo "   Type: $type"
    echo "   Location: $location"
    
    if [ "$type" = "PHYSICAL" ]; then
        echo "   ⚠️  PHYSICAL COLLECTION REQUIRED"
        echo "   📍 Collect from: $location"
        echo "   📅 Closing: 08 April 2026"
        
        # Calculate days remaining
        target=$(date -d "2026-04-08" +%s)
        now=$(date +%s)
        days=$(( ($target - $now) / 86400 ))
        echo "   ⏳ Days remaining: $days"
    else
        # Try to fetch digital documents
        echo "   🔍 Scanning $location..."
        # Add digital scanning logic here
        echo "   📄 Documents: Checking..."
    fi
    echo "----------------------------------------"
done

# Check Revenue Bridge
if curl -s http://localhost:8082/health > /dev/null 2>&1; then
    echo "   • Revenue Bridge (8082): 🟢 ONLINE"
else
    echo "   • Revenue Bridge (8082): 🔴 OFFLINE"
fi

# Add to morning routine
echo "$(date): Contract watch completed" >> logs/contract_watcher.log
