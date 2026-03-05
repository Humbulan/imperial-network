#!/usr/bin/env python3
"""
🏛️ IMPERIAL REVENUE TRACKER
Tracks all B2B transactions and receipts
"""
import json
import csv
from datetime import datetime, timedelta
from pathlib import Path
import sqlite3

class RevenueTracker:
    def __init__(self):
        self.audit_dir = Path.home() / 'imperial_network' / 'audits'
        self.receipts_file = self.audit_dir / 'revenue_log.json'
        self.load_revenue()
    
    def load_revenue(self):
        if self.receipts_file.exists():
            with open(self.receipts_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {
                'transactions': [],
                'total_revenue': 0,
                'vouchers_used': 0,
                'last_updated': datetime.now().isoformat()
            }
    
    def save_revenue(self):
        with open(self.receipts_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def add_transaction(self, company, contact, phone, amount=20, method='voucher', notes=''):
        """Record a new transaction"""
        transaction = {
            'id': f"IMP-TXN-{datetime.now().strftime('%Y%m%d')}-{len(self.data['transactions'])+1:04d}",
            'company': company,
            'contact': contact,
            'phone': phone,
            'amount': amount,
            'method': method,
            'timestamp': datetime.now().isoformat(),
            'notes': notes,
            'status': 'completed'
        }
        
        self.data['transactions'].append(transaction)
        self.data['total_revenue'] += amount
        self.data['vouchers_used'] += 1
        self.data['last_updated'] = datetime.now().isoformat()
        self.save_revenue()
        
        print(f"✅ Transaction recorded: +R{amount} from {company}")
        return transaction
    
    def generate_report(self):
        """Generate daily/weekly/monthly report"""
        now = datetime.now()
        today = now.date()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        
        daily = [t for t in self.data['transactions'] 
                if datetime.fromisoformat(t['timestamp']).date() == today]
        
        weekly = [t for t in self.data['transactions'] 
                 if datetime.fromisoformat(t['timestamp']) > week_ago]
        
        monthly = [t for t in self.data['transactions'] 
                  if datetime.fromisoformat(t['timestamp']) > month_ago]
        
        print("\n" + "="*60)
        print("🏛️ IMPERIAL REVENUE REPORT")
        print("="*60)
        print(f"📅 Generated: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\n💰 TOTAL REVENUE: R{self.data['total_revenue']:.2f}")
        print(f"🎫 VOUCHERS USED: {self.data['vouchers_used']}")
        print(f"\n📊 BREAKDOWN:")
        print(f"   Today ({today}): {len(daily)} transactions | R{sum(t['amount'] for t in daily):.2f}")
        print(f"   Last 7 days: {len(weekly)} transactions | R{sum(t['amount'] for t in weekly):.2f}")
        print(f"   Last 30 days: {len(monthly)} transactions | R{sum(t['amount'] for t in monthly):.2f}")
        
        print("\n📋 RECENT TRANSACTIONS:")
        for t in self.data['transactions'][-5:]:
            date = datetime.fromisoformat(t['timestamp']).strftime('%Y-%m-%d')
            print(f"   {date} | {t['company']:<20} | +R{t['amount']:.2f} | {t['contact']}")
        
        print("\n🎯 NEXT TARGETS:")
        targets = [
            "Mudau Logistics (5 trucks) - Contact: 0794658481",
            "Baloyi Transport (3 trucks) - Contact: 0822345678",
            "Nemadodzi Haulage (7 trucks) - Contact: 0829649626"
        ]
        for target in targets:
            print(f"   • {target}")
        
        print("="*60)
    
    def export_csv(self):
        """Export all transactions to CSV"""
        csv_file = self.audit_dir / f"revenue_export_{datetime.now().strftime('%Y%m%d')}.csv"
        
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Date', 'Company', 'Contact', 'Phone', 'Amount', 'Method', 'Notes'])
            
            for t in self.data['transactions']:
                date = datetime.fromisoformat(t['timestamp']).strftime('%Y-%m-%d')
                writer.writerow([
                    date,
                    t['company'],
                    t['contact'],
                    t['phone'],
                    t['amount'],
                    t['method'],
                    t['notes']
                ])
        
        print(f"✅ Revenue exported to: {csv_file}")
    
    def whatsapp_message(self, company):
        """Generate WhatsApp message for follow-up"""
        templates = {
            'Nemadodzi Haulage': "🇿🇦 *Nemadodzi Haulage - Beira Clearance*\n\nMr. Nemadodzi, here is your official receipt for the digital audit of your 7 trucks. The CSV file contains the full clearance certificate for Checkpoint 7.\n\n• Audit ID: AUD-20260225-NH002\n• Amount: R20.00\n• Status: PAID\n\nAttached: Receipt + Audit CSV\n\nReady for monthly bulk rate discussion?",
            
            'Mudau Logistics': "🇿🇦 *Mudau Logistics - Lithium Transport*\n\nMr. Mudau, your 5 lithium trucks are pre-cleared for Beira. Attached is the official receipt and audit certificate.\n\n• Fleet: 5 Scania/Volvo trucks\n• Cargo: 125 tonnes Lithium (UN 3090)\n• Status: AUTHORIZED",
            
            'Baloyi Transport': "🇿🇦 *Baloyi Transport - Agricultural Clearance*\n\nMr. Baloyi, your 3 trucks are cleared for Beira Berth 4. Receipt and audit attached.\n\n• Cargo: Mixed Agricultural\n• Checkpoint: 4\n• Status: CLEARED"
        }
        
        return templates.get(company, f"🇿🇦 *{company} - Beira Clearance*\n\nYour official receipt and audit certificate are attached.\n\nThank you for using Imperial Network.")

# Main execution
if __name__ == "__main__":
    tracker = RevenueTracker()
    
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == 'report':
            tracker.generate_report()
        elif sys.argv[1] == 'export':
            tracker.export_csv()
        elif sys.argv[1] == 'add' and len(sys.argv) >= 5:
            tracker.add_transaction(
                company=sys.argv[2],
                contact=sys.argv[3],
                phone=sys.argv[4],
                amount=int(sys.argv[5]) if len(sys.argv) > 5 else 20,
                notes=sys.argv[6] if len(sys.argv) > 6 else ''
            )
        elif sys.argv[1] == 'message' and len(sys.argv) > 2:
            msg = tracker.whatsapp_message(sys.argv[2])
            print("\n📱 WHATSAPP MESSAGE:")
            print("-"*40)
            print(msg)
            print("-"*40)
    else:
        tracker.generate_report()
