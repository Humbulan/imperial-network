#!/usr/bin/env python3
"""
🏛️ IMPERIAL LIGHTWEIGHT TOPIC ANALYZER
Simple keyword clustering without heavy dependencies
"""
import json
import re
from collections import defaultdict, Counter
from datetime import datetime

print("🏛️ IMPERIAL LIGHTWEIGHT TOPIC ANALYZER")
print("="*60)

# Load corpus
try:
    with open('lda_corpus.txt', 'r') as f:
        documents = [line.strip() for line in f if line.strip()]
    print(f"📚 Loaded {len(documents)} documents")
except FileNotFoundError:
    print("❌ lda_corpus.txt not found")
    exit(1)

# Simple keyword extraction
print("\n🔍 ANALYZING KEYWORDS...")

# Define topic categories and their keywords
topic_keywords = {
    'SADC_TRADE': ['logistics', 'corridor', 'lithium', 'gold', 'energy', 'beira', 'sadc', 'export', 'import'],
    'GOVERNMENT_SAAS': ['municipality', 'government', 'saas', 'audit', 'contract', 'recurring', 'service'],
    'MOBILE_PAYMENTS': ['mobile', 'momo', 'mtn', 'vodacom', 'ussd', 'sms', 'airtime', 'wallet'],
    'FINANCIAL_SETTLEMENTS': ['settlement', 'payment', 'transfer', 'batch', 'clearing', 'revenue'],
    'LOCAL_COMMERCE': ['spaza', 'shop', 'market', 'village', 'trader', 'artisan', 'goods']
}

# Count documents by topic
topic_counts = defaultdict(int)
topic_words = defaultdict(list)

for doc in documents:
    doc_lower = doc.lower()
    matched = False
    
    for topic, keywords in topic_keywords.items():
        for keyword in keywords:
            if keyword in doc_lower:
                topic_counts[topic] += 1
                topic_words[topic].extend([word for word in re.findall(r'\b\w+\b', doc_lower) if len(word) > 3])
                matched = True
                break
        if matched:
            break
    
    if not matched:
        topic_counts['OTHER'] += 1
        topic_words['OTHER'].extend([word for word in re.findall(r'\b\w+\b', doc_lower) if len(word) > 3])

# Get most common words per topic
topic_common_words = {}
for topic, words in topic_words.items():
    counter = Counter(words)
    topic_common_words[topic] = [word for word, _ in counter.most_common(10)]

# Load metadata
metadata = {}
try:
    with open('lda_metadata.json', 'r') as f:
        metadata = json.load(f)
except:
    metadata = {'total_records': len(documents)}

# Display results
print("\n🏛️ IMPERIAL TOPIC CLUSTERS")
print("="*60)

total = len(documents)
for topic, count in sorted(topic_counts.items(), key=lambda x: x[1], reverse=True):
    percentage = (count / total) * 100
    print(f"\n📌 {topic}: {count} documents ({percentage:.1f}%)")
    print(f"   Keywords: {', '.join(topic_common_words.get(topic, [])[:5])}")
    if len(topic_common_words.get(topic, [])) > 5:
        print(f"             {', '.join(topic_common_words.get(topic, [])[5:10])}")

# Summary
print("\n📊 ANALYSIS SUMMARY")
print("="*60)
print(f"📁 Total documents: {metadata.get('total_records', total)}")
print(f"💰 Total value: R{metadata.get('total_value', 0):,.2f}")
print(f"📊 Active topics: {len(topic_counts)}")

# Save results
results = {
    'topic_distribution': dict(topic_counts),
    'topic_keywords': topic_common_words,
    'total_documents': total,
    'timestamp': datetime.now().isoformat()
}

with open('imperial_topics.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\n✅ Analysis saved to: imperial_topics.json")
