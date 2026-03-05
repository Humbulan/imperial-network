#!/usr/bin/env python3
"""
🧠 IMPERIAL LDA TRAINER
Latent Dirichlet Allocation for transaction clustering
"""
import re
import json
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Try to import Gensim - install if not available
try:
    import gensim
    from gensim import corpora
    from gensim.models import LdaModel
    from gensim.parsing.preprocessing import STOPWORDS
    GENSIM_AVAILABLE = True
except ImportError:
    GENSIM_AVAILABLE = False
    print("⚠️ Gensim not installed. Installing...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'gensim'])
    import gensim
    from gensim import corpora
    from gensim.models import LdaModel
    from gensim.parsing.preprocessing import STOPWORDS

print("🧠 IMPERIAL LDA TRAINER")
print("="*60)

# Load corpus
try:
    with open('lda_corpus.txt', 'r') as f:
        documents = [line.strip() for line in f if line.strip()]
    print(f"📚 Loaded {len(documents)} documents for training")
except FileNotFoundError:
    print("❌ lda_corpus.txt not found. Run lda_data_extractor.py first.")
    exit(1)

# Custom stopwords (financial terms to preserve)
custom_stopwords = set(STOPWORDS) - {'R', 'payment', 'transaction', 'corridor'}

# Preprocess documents
print("\n🔧 PREPROCESSING DOCUMENTS...")
processed_docs = []
for doc in documents:
    # Tokenize and clean
    tokens = gensim.utils.simple_preprocess(str(doc), deacc=True)
    # Remove stopwords but preserve financial terms
    tokens = [token for token in tokens if token not in custom_stopwords and len(token) > 2]
    processed_docs.append(tokens)

# Create dictionary and corpus
print("📊 CREATING DOCUMENT TERM MATRIX...")
dictionary = corpora.Dictionary(processed_docs)
dictionary.filter_extremes(no_below=2, no_above=0.8)  # Filter rare/too common words

bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

print(f"  • Vocabulary size: {len(dictionary)} unique terms")

# Determine optimal number of topics
print("\n🎯 TRAINING LDA MODELS...")

# Try different topic numbers
topic_results = []
for num_topics in [3, 4, 5, 6]:
    print(f"  Training {num_topics}-topic model...")
    lda_model = LdaModel(
        corpus=bow_corpus,
        id2word=dictionary,
        num_topics=num_topics,
        random_state=42,
        update_every=1,
        chunksize=100,
        passes=10,
        alpha='auto',
        per_word_topics=True
    )
    
    # Calculate coherence score
    coherence_model = gensim.models.CoherenceModel(
        model=lda_model, 
        texts=processed_docs, 
        dictionary=dictionary, 
        coherence='c_v'
    )
    coherence_score = coherence_model.get_coherence()
    topic_results.append((num_topics, coherence_score, lda_model))
    
    print(f"     Coherence: {coherence_score:.4f}")

# Select best model
best_topics, best_score, best_model = max(topic_results, key=lambda x: x[1])
print(f"\n🏆 BEST MODEL: {best_topics} topics (coherence: {best_score:.4f})")

# Display topics
print("\n📋 TOPIC CLUSTERS:")
print("="*60)

imperial_clusters = {}
for idx, topic in best_model.print_topics(num_words=10):
    # Parse topic words
    words = re.findall(r'"([^"]*)"', topic)
    print(f"\n🎯 TOPIC {idx + 1}:")
    print(f"   Words: {', '.join(words[:5] + ['...'])}")
    print(f"   Full: {topic[:100]}...")
    
    # Categorize based on keywords
    if any(w in ' '.join(words) for w in ['lithium', 'energy', 'gold', 'logistics', 'corridor']):
        category = "SADC TRADE"
    elif any(w in ' '.join(words) for w in ['municipality', 'saas', 'audit', 'government']):
        category = "GOVERNMENT SAAS"
    elif any(w in ' '.join(words) for w in ['mobile', 'momo', 'ussd', 'payment']):
        category = "MOBILE PAYMENTS"
    else:
        category = "GENERAL TRANSACTIONS"
    
    imperial_clusters[f"TOPIC_{idx+1}"] = {
        'category': category,
        'keywords': words[:10],
        'weight': 1.0
    }

# Analyze document-topic distribution
print("\n📊 DOCUMENT-TOPIC DISTRIBUTION:")
doc_topics = []
for i, bow in enumerate(bow_corpus[:100]):  # Sample first 100
    topic_dist = best_model.get_document_topics(bow)
    if topic_dist:
        main_topic = max(topic_dist, key=lambda x: x[1])
        doc_topics.append(main_topic[0])

# Count documents per topic
topic_counts = np.bincount(doc_topics) if doc_topics else []
for i, count in enumerate(topic_counts):
    print(f"  Topic {i+1}: {count} documents ({count/len(doc_topics)*100:.1f}%)")

# Save model and results
print("\n💾 SAVING MODEL...")
best_model.save('imperial_lda_model')
dictionary.save('lda_dictionary')

# Save topic clusters
with open('imperial_clusters.json', 'w') as f:
    json.dump(imperial_clusters, f, indent=2)

print("✅ Model saved to: imperial_lda_model")
print("✅ Dictionary saved to: lda_dictionary")
print("✅ Clusters saved to: imperial_clusters.json")

# Generate visualization data
print("\n📈 GENERATING VISUALIZATION...")
vis_data = {
    'num_topics': best_topics,
    'coherence_score': best_score,
    'topics': imperial_clusters,
    'timestamp': datetime.now().isoformat()
}

with open('lda_visualization.json', 'w') as f:
    json.dump(vis_data, f, indent=2)

print("\n✅ LDA training complete")
print("   Run 'python3 lda_visualizer.py' to view results")
