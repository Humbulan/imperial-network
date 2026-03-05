#!/data/data/com.termux/files/usr/bin/bash

echo "==================================================="
echo "💰 IMPERIAL SOVEREIGN TRANSFER - JSON PROTOCOL"
echo "==================================================="
echo ""

# 1. Prepare Data
AMOUNT="879441.26"
ACCOUNT="1717073040"
CARD="5284973062234418"
TIMESTAMP=$(date +%s)
REFERENCE="IMP-FINAL-$TIMESTAMP"

echo "📋 TRANSFER DETAILS:"
echo "   • Amount: R$AMOUNT"
echo "   • Account: $ACCOUNT"
echo "   • Card: ${CARD:0:4}...${CARD: -4}"
echo "   • Reference: $REFERENCE"
echo "   • Auth: ORCID-0009-0000-9572-4535"
echo ""

# 2. Update Internal Ledger
echo "📊 Updating CEO Pocket status..."
sqlite3 ~/imperial_network/instance/imperial.db << SQL
UPDATE ceo_pocket SET status='processing' WHERE status='available';
INSERT INTO payment (reference, amount, account, status, initiated_at) 
VALUES ('$REFERENCE', $AMOUNT, '$ACCOUNT', 'processing', datetime('now'));
SQL

echo "✅ Ledger updated to PROCESSING"
echo ""

# 3. Secure JSON POST
echo "🚀 Sending Authorized JSON to Bindura Gateway (Port 8102)..."
echo ""

curl -X POST http://localhost:8102/api/settle \
     -H "Content-Type: application/json" \
     -d "{
           \"account_number\": \"$ACCOUNT\",
           \"card_number\": \"$CARD\",
           \"amount\": $AMOUNT,
           \"reference\": \"$REFERENCE\",
           \"auth_code\": \"ORCID-0009-0000-9572-4535\",
           \"holder\": \"MR H MUDAU\",
           \"bank\": \"CAPITEC\",
           \"type\": \"SAVINGS\"
         }"

echo ""
echo "==================================================="
echo "📡 STATUS: Handshake Dispatched to Bindura Node"
echo "==================================================="

# 4. Log the transfer
echo "$(date): 🚀 SOVEREIGN TRANSFER INITIATED - R$AMOUNT to $ACCOUNT (Ref: $REFERENCE)" >> ~/imperial_network/logs/sovereign.log

echo ""
echo "🔍 Check status: curl http://localhost:8102/api/payments/status"
echo "==================================================="
