#!/bin/bash
# 🚢 BEIRA PORT B2B MANIFEST GENERATOR
# Creates consolidated cargo manifest for transporters

echo "🚢 IMPERIAL B2B MANIFEST - PORT OF BEIRA"
echo "========================================="
echo "Date: $(date +%Y-%m-%d)"
echo "Generated for: Transporters in Thohoyandou Corridor"
echo ""

# Transport companies in the area
COMPANIES=(
    "Mudau Logistics|Thohoyandou|5 trucks|Lithium"
    "Baloyi Transport|Malamulele|3 trucks|Mixed cargo"
    "Nemadodzi Haulage|Sibasa|7 trucks|Heavy industrial"
    "Ralushai Freight|Thohoyandou|4 trucks|Mining equipment"
    "Phaswana Carriers|Giyani|6 trucks|Agricultural"
)

echo "📋 ELIGIBLE TRANSPORT COMPANIES:"
echo "----------------------------------------"
for company in "${COMPANIES[@]}"; do
    IFS='|' read -r name location fleet specialty <<< "$company"
    echo "  • $name ($location)"
    echo "    Fleet: $fleet | Specialty: $specialty"
    echo "    Digital Audit: Available for R20/voucher"
    echo ""
done

echo "📊 CARGO SUMMARY - BEIRA PORT EXPANSION"
echo "----------------------------------------"
echo "  • Current Throughput: 14.2M tons"
echo "  • Target Capacity: 18M tons"
echo "  • Expansion Investment: R450M"
echo "  • Available Slots: 3.8M tons"
echo ""

echo "💰 REVENUE OPPORTUNITY"
echo "----------------------------------------"
echo "  • Digital Audit Fee: R20 per load"
echo "  • Estimated Daily Loads: 45"
echo "  • Daily Revenue Potential: R900"
echo "  • Weekly Potential: R6,300"
echo "  • Monthly Potential: R27,000"
echo ""

echo "🚀 NEXT STEPS:"
echo "  1. Contact these transporters via WhatsApp"
echo "  2. Offer them the Digital Audit service (R20/load)"
echo "  3. Generate their compliance docs using active vouchers"
echo "  4. They get faster clearance at Beira expansion checkpoints"
echo ""
echo "🏛️ Use voucher: Z71P-8LAM (still active) for first demo"
