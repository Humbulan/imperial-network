#!/usr/bin/env python3
"""
Test migrated components in Imperial Network
"""
import sys
from pathlib import Path

print("🏛️ TESTING MIGRATED COMPONENTS")
print("=" * 60)

# Add migrated directories to path
migrated_base = Path("migrated")
sys.path.insert(0, str(migrated_base))

# Test importing core components
print("\n📦 Testing Priority 1 - Core Infrastructure:")
core_modules = [
    "master_orchestrator",
    "revenue_bridge",
    "ussd_interface",
    "government_api"
]

for module in core_modules:
    try:
        __import__(f"priority1_core.{module}")
        print(f"   ✅ {module}.py imported successfully")
    except Exception as e:
        print(f"   ⚠️  {module}.py: {e}")

# Test financial modules
print("\n💰 Testing Priority 2 - Financial Systems:")
finance_modules = [
    "transaction_engine_secure",
    "merchant_payouts",
    "mobile_money_integration"
]

for module in finance_modules:
    try:
        __import__(f"priority2_financial.{module}")
        print(f"   ✅ {module}.py imported successfully")
    except Exception as e:
        print(f"   ⚠️  {module}.py: {e}")

# Check data files
print("\n📊 Verifying Data Files:")
data_files = [
    "migrated/data/transactions.csv",
    "migrated/data/council_pins_distribution.csv",
    "migrated/data/community_nexus.db",
    "migrated/data/vault.db",
    "migrated/configs/gauteng_nodes.json"
]

for file in data_files:
    if Path(file).exists():
        size = Path(file).stat().st_size
        print(f"   ✅ {file} ({size} bytes)")
    else:
        print(f"   ⚠️  {file} not found")

print("\n" + "=" * 60)
print("🏁 Migration test complete!")
