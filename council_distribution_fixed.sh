#!/bin/bash
# 🏛️ COUNCIL ALPHA DISTRIBUTION - VILLAGE BREAKDOWN

echo "🏛️ IMPERIAL COUNCIL ALPHA DISTRIBUTION"
echo "========================================"

# Calculate village distributions
sqlite3 instance/imperial.db << SQL
.mode column
.headers on
WITH village_data AS (
    SELECT 
        CASE 
            WHEN member_id LIKE 'THO%' THEN 'Thohoyandou'
            WHEN member_id LIKE 'SIB%' THEN 'Sibasa'
            WHEN member_id LIKE 'MAL%' THEN 'Malamulele'
            WHEN member_id LIKE 'LWM%' THEN 'Lwamondo'
            WHEN member_id LIKE 'MAN%' THEN 'Manini'
            ELSE 'Other'
        END as village,
        COUNT(*) as members,
        SUM(allocation) as base_total,
        SUM(allocation) * 1.25 as alpha_total
    FROM council_pins
    GROUP BY village
    ORDER BY alpha_total DESC
)
SELECT 
    village AS "Village",
    members AS "Members",
    printf('R%.2f', base_total) AS "Base Fund",
    printf('R%.2f', alpha_total) AS "With Alpha"
FROM village_data;
SQL

echo ""
echo "💰 TOTAL SUMMARY:"
sqlite3 instance/imperial.db << SQL
SELECT 
    'Total Members: ' || COUNT(*) || 
    ' | Base Fund: R' || printf('%.2f', SUM(allocation)) || 
    ' | With Alpha: R' || printf('%.2f', SUM(allocation)*1.25)
FROM council_pins;
SQL

echo ""
echo "🚀 EXECUTION COMMAND:"
echo "   To mark all as distributed, run:"
echo "   sqlite3 instance/imperial.db \"UPDATE council_pins SET status='distributed' WHERE status='active';\""
echo ""
echo "💬 NOTIFICATION PREVIEWS:"
echo "   🏔️ Tshivenda: $(cat notifications/council_ve.txt 2>/dev/null | sed 's/{amount}/25.80/')"
echo "   🌊 Xitsonga:  $(cat notifications/council_ts.txt 2>/dev/null | sed 's/{amount}/25.80/')"
echo "   🇬🇧 English:   $(cat notifications/council_en.txt 2>/dev/null | sed 's/{amount}/25.80/')"
