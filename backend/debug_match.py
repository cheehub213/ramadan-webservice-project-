"""Debug matching"""
from services_quran_semantic import QuranSemanticSearch

# Initialize
QuranSemanticSearch.load_model()

# Test query
query = "I am angry at my family"
prompt_vector = QuranSemanticSearch.model.encode(query)
prompt_lower = query.lower()

print(f"Query: {query}")
print(f"Query lower: {prompt_lower}")
print("\nScores for each verse:")

import numpy as np

for verse in QuranSemanticSearch.KEY_VERSES:
    verse_vector = QuranSemanticSearch.model.encode(verse["text_en"])
    semantic_sim = np.dot(prompt_vector, verse_vector) / (
        np.linalg.norm(prompt_vector) * np.linalg.norm(verse_vector) + 1e-10
    )
    
    # Check keywords
    keyword_boost = 0
    matched_topic = None
    for topic in verse.get("topics", []):
        if topic in prompt_lower:
            keyword_boost = 0.35
            matched_topic = topic
            break
    
    final = semantic_sim + keyword_boost
    
    ref = verse["ref"]
    topics = verse["topics"]
    print(f"{ref:10} | Sem: {semantic_sim:.3f} | Keywords: {topics} | Boost: {keyword_boost:.2f} | Final: {final:.3f} | Match: {matched_topic}")
