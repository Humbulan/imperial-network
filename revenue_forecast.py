#!/usr/bin/env python3
"""
Imperial Omega Revenue Forecast Calculator
Projects R500M target based on active revenue streams
"""
from datetime import datetime, timedelta
import json

# Current secured assets (from your verified data)
current_portfolio = 10938044.07  # R10,938,044.07 from Absolute Truth
leda_partnership = 15700000.00    # R15.7M LEDA partnership
monthly_saas_usd = 147575.00      # $147,575 monthly SaaS
usd_to_zar = 18.50                 # Current exchange rate (approximate)

# Calculate monthly ZAR income
monthly_saas_zar = monthly_saas_usd * usd_to_zar  # ~R2,730,137.50

# Other secured grants
nyda_grant = 300000.00
sefa_trep = 1000000.00

# Total secured base
secured_base = current_portfolio + leda_partnership + nyda_grant + sefa_trep

target = 500000000.00
remaining = target - secured_base

print("\n" + "="*60)
print("🏛️  IMPERIAL OMEGA REVENUE FORECAST")
print("="*60)
print(f"\n📊 CURRENT SECURED ASSETS:")
print(f"   • Portfolio Value:      R{current_portfolio:>13,.2f}")
print(f"   • LEDA Partnership:     R{leda_partnership:>13,.2f}")
print(f"   • NYDA Youth Grant:     R{nyda_grant:>13,.2f}")
print(f"   • SEFA TREP:            R{sefa_trep:>13,.2f}")
print(f"   {'='*42}")
print(f"   TOTAL SECURED:          R{secured_base:>13,.2f}")
print(f"\n🎯 TARGET:                 R{target:>13,.2f}")
print(f"📉 REMAINING:              R{remaining:>13,.2f}")
print(f"\n💵 MONTHLY SaaS INCOME:    ${monthly_saas_usd:>11,.2f} USD")
print(f"                         ≈ R{monthly_saas_zar:>11,.2f} ZAR")

# Calculate time to target with current monthly income
months_to_target = remaining / monthly_saas_zar
years = months_to_target / 12
target_date = datetime.now() + timedelta(days=months_to_target*30)

print(f"\n⏱️  PROJECTED TIMELINE (at current velocity):")
print(f"   • Months to target:     {months_to_target:>8.1f}")
print(f"   • Years to target:      {years:>8.2f}")
print(f"   • Target date:          {target_date.strftime('%Y-%m-%d')}")

# Milestone projections
milestones = [0.05, 0.10, 0.25, 0.50, 0.75, 1.0]
print(f"\n🎯 MILESTONE PROJECTIONS:")
milestone_data = []

for milestone in milestones:
    milestone_value = target * milestone
    milestone_remaining = milestone_value - secured_base
    
    if milestone_remaining > 0:
        milestone_months = milestone_remaining / monthly_saas_zar
        milestone_date = datetime.now() + timedelta(days=milestone_months*30)
        date_str = milestone_date.strftime('%Y-%m-%d')
        print(f"   • {milestone*100:>3.0f}% (R{milestone_value:>11,.0f}): {date_str} ({milestone_months:>5.1f} months)")
        milestone_data.append({
            "percent": milestone*100,
            "value": milestone_value,
            "date": date_str,
            "months": milestone_months
        })
    else:
        print(f"   • {milestone*100:>3.0f}% (R{milestone_value:>11,.0f}): ✅ ALREADY ACHIEVED")
        milestone_data.append({
            "percent": milestone*100,
            "value": milestone_value,
            "date": "ACHIEVED",
            "months": 0
        })

# Save forecast to file
forecast = {
    "timestamp": datetime.now().isoformat(),
    "secured_base": secured_base,
    "target": target,
    "remaining": remaining,
    "monthly_income_zar": monthly_saas_zar,
    "months_to_target": months_to_target,
    "target_date": target_date.strftime('%Y-%m-%d'),
    "milestones": milestone_data
}

with open('revenue_forecast.json', 'w') as f:
    json.dump(forecast, f, indent=2)

print("\n📁 Forecast saved to: revenue_forecast.json")
print("="*60)
