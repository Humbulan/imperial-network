#!/usr/bin/env python3
"""
📊 IMPERIAL LDA VISUALIZER
Display thematic clusters in a clean format
"""
import json
from datetime import datetime

print("📊 IMPERIAL LDA VISUALIZER")
print("="*60)

try:
    with open('imperial_clusters.json', 'r') as f:
        clusters = json.load(f)
except FileNotFoundError:
    print("❌ imperial_clusters.json not found. Run lda_training.py first.")
    exit(1)

print("\n🏛️ IMPERIAL THEMATIC CLUSTERS")
print("="*60)

for topic_id, topic_data in clusters.items():
    print(f"\n{topic_id}: {topic_data['category']}")
    print("-" * 40)
    print(f"  Keywords: {', '.join(topic_data['keywords'][:5])}")
    if len(topic_data['keywords']) > 5:
        print(f"            {', '.join(topic_data['keywords'][5:10])}")

# Load metadata
try:
    with open('lda_metadata.json', 'r') as f:
        metadata = json.load(f)
    
    print("\n📊 DATA METADATA")
    print("-" * 40)
    print(f"  Records analyzed: {metadata['total_records']:,}")
    if 'total_value' in metadata and metadata['total_value'] > 0:
        print(f"  Total value: R{metadata['total_value']:,.2f}")
    print(f"  Payment methods: {len(metadata.get('by_method', {}))}")
    
    if metadata.get('by_method'):
        print("\n  Top payment methods:")
        for method, count in list(metadata['by_method'].items())[:5]:
            print(f"    • {method}: {count}")

except FileNotFoundError:
    print("\nℹ️ No metadata available")

print("\n✅ LDA analysis complete")
