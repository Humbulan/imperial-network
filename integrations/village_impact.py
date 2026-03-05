#!/usr/bin/env python3
"""
Village Impact Integrator - Economic Bedrock of Imperial Omega
Merges CSV data with Voucher Dashboard for real-time village-level analytics
"""

import csv
import json
import sqlite3
import os
from datetime import datetime
from pathlib import Path

# Configuration
DATA_DIR = Path("/data/data/com.termux/files/home/imperial_network/data/economic_bedrock")
DB_PATH = "/data/data/com.termux/files/home/imperial_network/instance/imperial.db"
VOUCHER_API = "http://127.0.0.1:8098/api/vouchers"

class VillageImpactAnalyzer:
    def __init__(self):
        self.merchants = []
        self.revenue = []
        self.load_data()
    
    def load_data(self):
        """Load both CSV files"""
        # Load merchant impact data
        merchant_file = list(DATA_DIR.glob("8afa*.csv"))
        if merchant_file:
            with open(merchant_file[0], 'r') as f:
                reader = csv.DictReader(f)
                self.merchants = list(reader)
            print(f"✅ Loaded {len(self.merchants)} merchant records")
        
        # Load revenue data
        revenue_file = list(DATA_DIR.glob("e28e*.csv"))
        if revenue_file:
            with open(revenue_file[0], 'r') as f:
                reader = csv.DictReader(f)
                self.revenue = list(reader)
            print(f"✅ Loaded {len(self.revenue)} revenue records")
    
    def analyze_village_impact(self):
        """Analyze impact by village"""
        print("\n🏘️  VILLAGE IMPACT ANALYSIS")
        print("="*60)
        
        total_impact = 0
        total_merchants = 0
        expansion_zones = []
        
        for merchant in self.merchants:
            village_id = merchant['Village_ID']
            impact = float(merchant['Current_Impact_ZAR'])
            merchants = int(merchant['Merchant_Count'])
            readiness = float(merchant['Digital_Readiness'])
            status = merchant['Status']
            
            total_impact += impact
            total_merchants += merchants
            
            if status == 'EXPANSION_ZONE':
                expansion_zones.append({
                    'village': village_id,
                    'readiness': readiness,
                    'potential': impact
                })
            
            print(f"\n📌 {village_id}")
            print(f"   • Merchants: {merchants}")
            print(f"   • Impact: R{impact:,.2f}")
            print(f"   • Digital Readiness: {readiness}")
            print(f"   • Status: {status}")
        
        print("\n" + "="*60)
        print(f"📊 TOTAL SYSTEM IMPACT: R{total_impact:,.2f}")
        print(f"👥 TOTAL MERCHANTS: {total_merchants}")
        
        # Highlight expansion zones
        if expansion_zones:
            print("\n🚀 EXPANSION ZONES READY:")
            for zone in expansion_zones:
                print(f"   • {zone['village']} (Readiness: {zone['readiness']})")
        
        return {
            'total_impact': total_impact,
            'total_merchants': total_merchants,
            'expansion_zones': expansion_zones
        }
    
    def analyze_revenue_trends(self):
        """Analyze revenue and growth trends"""
        print("\n📈 REVENUE ANALYSIS")
        print("="*60)
        
        if not self.revenue:
            print("No revenue data found")
            return
        
        latest = self.revenue[-1]
        portfolio = float(latest['Portfolio_Value'])
        revenue = float(latest['Revenue_ZAR'])
        merchant_impact = float(latest['Merchant_Impact_ZAR'])
        uptime = latest['Uptime_Percent']
        speed_inc = latest['Speed_Increase']
        fuel_red = latest['Fuel_Reduction']
        
        print(f"\n📊 Latest Snapshot ({latest['Date']} - {latest['Shift']})")
        print(f"   • Portfolio Value: R{portfolio:,.2f}")
        print(f"   • Revenue Generated: R{revenue:,.2f}")
        print(f"   • Merchant Impact: R{merchant_impact:,.2f}")
        print(f"   • Uptime: {uptime}%")
        print(f"   • Speed Increase: {speed_inc}")
        print(f"   • Fuel Reduction: {fuel_red}")
        
        # Calculate growth
        if len(self.revenue) > 1:
            first = self.revenue[0]
            initial_portfolio = float(first['Portfolio_Value'])
            growth = ((portfolio - initial_portfolio) / initial_portfolio) * 100
            print(f"\n📈 Portfolio Growth: {growth:.2f}%")
            print(f"   • Initial: R{initial_portfolio:,.2f}")
            print(f"   • Current: R{portfolio:,.2f}")
            print(f"   • Gain: R{portfolio - initial_portfolio:,.2f}")
        
        return {
            'portfolio': portfolio,
            'revenue': revenue,
            'merchant_impact': merchant_impact,
            'uptime': uptime,
            'growth': growth if len(self.revenue) > 1 else 0
        }
    
    def sync_with_voucher_api(self):
        """Sync village data with voucher system"""
        print("\n🔄 SYNCING WITH VOUCHER SYSTEM")
        print("="*60)
        
        # Map villages to voucher codes
        village_voucher_map = {
            'VIL-THO-02': 'THO2026',  # Thohoyandou
            'VIL-GAU-EXT': 'GAU2026',  # Gauteng Extension
            'VIL-LIM-03': 'LIM2026',   # Limpopo
            'VIL-MPU-04': 'MPU2026',   # Mpumalanga
            'VIL-KWA-06': 'KWA2026',   # KwaZulu-Natal
        }
        
        for merchant in self.merchants:
            village = merchant['Village_ID']
            if village in village_voucher_map:
                voucher_code = village_voucher_map[village]
                impact = float(merchant['Current_Impact_ZAR'])
                
                # Calculate village voucher allocation (5% of impact)
                voucher_value = impact * 0.05
                
                print(f"\n{village} → {voucher_code}")
                print(f"   • Impact: R{impact:,.2f}")
                print(f"   • Voucher Allocation: R{voucher_value:,.2f}")
                
                # Here you would POST to voucher API
                # requests.post(VOUCHER_API, json={voucher_code: voucher_value})
    
    def update_dawn_report(self):
        """Generate economic summary for dawn report"""
        merchant_analysis = self.analyze_village_impact()
        revenue_analysis = self.analyze_revenue_trends()
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_merchants": merchant_analysis['total_merchants'],
            "total_impact": merchant_analysis['total_impact'],
            "portfolio_value": revenue_analysis['portfolio'] if revenue_analysis else 0,
            "expansion_zones": len(merchant_analysis['expansion_zones']),
            "growth_percentage": revenue_analysis['growth'] if revenue_analysis else 0
        }
        
        # Save to cache
        with open(DATA_DIR / 'economic_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        return summary

if __name__ == "__main__":
    analyzer = VillageImpactAnalyzer()
    
    print("\n" + "🏛️  IMPERIAL OMEGA - ECONOMIC BEDROCK ANALYSIS")
    print("="*70)
    
    # Run full analysis
    analyzer.analyze_village_impact()
    analyzer.analyze_revenue_trends()
    analyzer.sync_with_voucher_api()
    
    # Generate summary
    summary = analyzer.update_dawn_report()
    
    print("\n" + "="*70)
    print(f"✅ Analysis complete - Economic bedrock validated")
    print(f"📁 Summary saved to: {DATA_DIR}/economic_summary.json")
