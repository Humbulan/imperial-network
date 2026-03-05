#!/usr/bin/env python3
"""
Simple ASCII Visualizer for SADC Trade Manifest
"""
import json
from datetime import datetime

try:
    with open('sadc_trade_manifest_20260223.json', 'r') as f:
        manifest = json.load(f)
    
    print("\n🏛️ SADC TRADE MANIFEST VISUALIZATION")
    print("=" * 60)
    print(f"Date: {manifest['timestamp'][:10]}")
    print(f"Total Volume: R{manifest['total_volume']:,.2f}")
    print(f"Throughput: {manifest['peak_throughput']:.1f} tx/sec")
    
    # Commodity distribution
    print("\n💎 COMMODITY DISTRIBUTION:")
    total = manifest['total_volume']
    for commodity, value in manifest['commodity_mix'].items():
        percentage = (value / total) * 100
        bar_length = int(percentage / 5)
        bar = "▓" * bar_length + "░" * (20 - bar_length)
        print(f"  {commodity.title():10} {bar} {percentage:5.1f}%")
    
    # Performance metrics
    print("\n⚡ PERFORMANCE METRICS:")
    latency = manifest['latency_p95']
    latency_bar = "▓" * int(latency / 10) if latency else 0
    print(f"  P95 Latency: {latency_bar} {latency:.0f}ms")
    
    throughput = manifest['peak_throughput']
    throughput_bar = "▓" * int(throughput)
    print(f"  Throughput:  {throughput_bar} {throughput:.1f} tx/sec")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"🏛️ IMPERIAL NETWORK: {manifest['trades_processed']} trades processed")
    print(f"💰 Value Created: R{manifest['total_volume']:,.2f}")
    print("=" * 60)
    
except FileNotFoundError:
    print("⚠️ No manifest found. Run the stress test first.")
except Exception as e:
    print(f"⚠️ Error: {e}")
