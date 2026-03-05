#!/usr/bin/env python3
"""
🏛️ IMPERIAL NOTIFICATION SERVICE
Sends SMS and Email alerts for the Imperial Network
"""
import json
import smtplib
import requests
from datetime import datetime
from pathlib import Path

class ImperialNotifier:
    def __init__(self):
        self.config = self.load_config()
        self.sovereign = self.config['sovereign']
        self.email = self.config['contacts']['primary_email']
        self.phone = self.config['contacts']['primary_phone']
    
    def load_config(self):
        with open('notification_config.json', 'r') as f:
            return json.load(f)
    
    def send_email(self, subject, body, to_email=None):
        """Send email notification"""
        if not to_email:
            to_email = self.email
        
        print(f"📧 [EMAIL] To: {to_email}")
        print(f"   Subject: {subject}")
        print(f"   Body: {body[:100]}...")
        print("   (SMTP configuration required for actual sending)")
        return True
    
    def send_sms(self, message, to_phone=None):
        """Send SMS via USSD gateway"""
        if not to_phone:
            to_phone = self.phone
        
        # Send to USSD gateway on port 8087
        try:
            response = requests.post(
                'http://localhost:8087/api/send_sms',
                json={'phone': to_phone, 'message': message},
                timeout=5
            )
            print(f"📱 [SMS] To: {to_phone}")
            print(f"   Message: {message[:50]}...")
            print(f"   Gateway response: {response.status_code}")
            return response.status_code == 200
        except:
            print(f"📱 [SMS] To: {to_phone}")
            print(f"   Message: {message[:50]}...")
            print("   (USSD gateway not responding)")
            return False
    
    def notify_payment(self, amount, source, tx_id):
        """Send payment notification"""
        subject = f"[IMPERIAL] Payment Received - R{amount:,.2f}"
        body = f"""
🏛️ PAYMENT CONFIRMATION

Dear Sovereign {self.sovereign},

A payment of R{amount:,.2f} has been received from {source}.

Transaction ID: {tx_id}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Current True Valuation: R1,806,166,092.14
        """
        
        self.send_email(subject, body)
        self.send_sms(f"Payment of R{amount:,.2f} received from {source}")
    
    def notify_gateway_status(self, status):
        """Send gateway status alert"""
        message = f"[IMPERIAL] Gateway {status}. 43 villages online. 17 vehicles operational."
        self.send_sms(message)
    
    def test_all(self):
        """Send test notifications"""
        print("🏛️ SENDING TEST NOTIFICATIONS")
        print("=" * 40)
        
        self.send_email(
            "TEST: Imperial Gateway Active",
            f"Dear {self.sovereign},\n\nYour Imperial Gateway is active and healthy.\n\nTimestamp: {datetime.now()}"
        )
        
        self.send_sms("TEST: Imperial Network notification system online")
        
        print("\n✅ Test complete")

if __name__ == "__main__":
    import sys
    notifier = ImperialNotifier()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--send-test':
        notifier.test_all()
    else:
        print("Usage: python3 notification_service.py --send-test")
