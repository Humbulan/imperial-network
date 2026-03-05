#!/usr/bin/env python3
"""
SADC Stress Test Visualizer
"""
import json
import matplotlib.pyplot as plt
from datetime import datetime

# Load manifest
with open('sadc_trade_manifest_20260223.json', 'r') as f:
    manifest = json.load(f)

print("🏛️ SADC TRADE MANIFEST VISUALIZATION")
print("=" * 60)
print(f"Date: {manifest['timestamp'][:10]}")
print(f"Total Volume: R{manifest['total_volume']:,.2f}")
print(f"Throughput: {manifest['peak_throughput']:.1f} tx/sec")

# Create ASCII visualization
print("\n💎 COMMODITY DISTRIBUTION:")
total = manifest['total_volume']
for commodity, value in manifest['commodity_mix'].items():
    percentage = (value / total) * 100
    bar = "▓" * int(percentage / 5) + "░" * (20 - int(percentage / 5))
    print(f"  {commodity.title():10} {bar} {percentage:5.1f}%")

print("\n⚡ PERFORMANCE METRICS:")
latency_bar = "▓" * int(manifest['latency_p95'] / 10)
print(f"  P95 Latency: {latency_bar} {manifest['latency_p95']:.0f}ms")

throughput_bar = "▓" * int(manifest['peak_throughput'])
print(f"  Throughput:  {throughput_bar} {manifest['peak_throughput']:.1f} tx/sec")
