"""
Semantic search for Quran verses - prioritizes keyword matches then semantic similarity
"""
from typing import List, Dict, Optional

try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
except ImportError:
    raise

class QuranSemanticSearch:
    """Semantic search matching user prompts to Quran verses"""
    
    model = None
    
    # Key verses with keywords for matching
    KEY_VERSES = [
        {"ref": "30:21", "surah": 30, "ayah": 21, "text_en": "And of His signs is that He created for you from yourselves mates that you may find tranquillity in them; and He placed between you affection and mercy.", "keywords": ["marriage", "spouse", "wife", "husband", "improve marriage"]},
        {"ref": "3:134", "surah": 3, "ayah": 134, "text_en": "Who spend [in the cause of Allah] during ease and hardship and who restrain anger and who pardon the people - and Allah loves the doers of good", "keywords": ["anger", "angry", "furious", "control", "restrain"]},
        {"ref": "65:3", "surah": 65, "ayah": 3, "text_en": "And will provide for him from where he does not expect. And whoever relies upon Allah - then He is sufficient for him.", "keywords": ["money", "poor", "wealth", "no money", "financially", "provision"]},
        {"ref": "94:5-6", "surah": 94, "ayah": 5, "text_en": "For indeed, with hardship [will be] ease. Indeed, with hardship [will be] ease.", "keywords": ["sad", "sadness", "depression", "depressed", "unhappy", "feel sad"]},
        {"ref": "17:23", "surah": 17, "ayah": 23, "text_en": "Your Lord has decreed that you not worship except Him, and to parents, good treatment. Whether one or both of them reach old age while with you, say not to them a word of disrespect.", "keywords": ["parents", "mother", "father", "elderly", "old"]},
        {"ref": "2:155-157", "surah": 2, "ayah": 155, "text_en": "And We will surely test you with something of fear and hunger and a loss of wealth and lives and fruits, but give good tidings to the patient. Who, when disaster strikes them, say, 'Indeed we belong to Allah, and indeed to Him we will return.'", "keywords": ["patience", "test", "difficult", "struggling", "patience"]},
        {"ref": "39:53", "surah": 39, "ayah": 53, "text_en": "Say, 'O My servants who have transgressed against themselves! Do not despair of the mercy of Allah. Indeed, Allah forgives all sins. Indeed, it is He who is the Forgiving, the Merciful.'", "keywords": ["forgiveness", "sin", "repent", "forgive", "guilt"]},
        {"ref": "2:286", "surah": 2, "ayah": 286, "text_en": "Allah does not burden a soul beyond that it can bear. It will have [the consequence of] what [good] it has earned, and it will bear [the consequence of] what [evil] it has earned.", "keywords": ["fear", "anxiety", "worry", "burden", "overwhelmed"]},
        {"ref": "29:69", "surah": 29, "ayah": 69, "text_en": "Those who strive for Us - We will surely guide them to Our paths. And indeed, Allah is with the righteous.", "keywords": ["alone", "loneliness", "isolated", "guidance"]},
        {"ref": "3:185", "surah": 3, "ayah": 185, "text_en": "Every soul will taste death. And you will only be given your full compensation on the Day of Resurrection. So whoever is drawn away from the Fire and admitted to Paradise has certainly succeeded.", "keywords": ["death", "died", "loss", "grief"]},
        {"ref": "9:105", "surah": 9, "ayah": 105, "text_en": "And say, 'Do [as you will], for Allah will see your deeds, and [so, too, will] His Messenger and the believers.'", "keywords": ["work", "job", "career", "success"]},
        {"ref": "4:32", "surah": 4, "ayah": 32, "text_en": "And do not wish for that by which Allah has made some of you exceed others. For men is a share of what they have earned, and for women is a share of what they have earned.", "keywords": ["jealous", "envy", "comparing", "jealousy"]},
        {"ref": "2:2-3", "surah": 2, "ayah": 2, "text_en": "This is the Book about which there is no doubt, a guidance for those conscious of Allah - Who believe in the unseen, establish prayer, and spend out of what We have provided for them.", "keywords": ["faith", "believe", "doubt", "trust"]},
        {"ref": "12:87", "surah": 12, "ayah": 87, "text_en": "Never lose hope in the mercy of Allah. Certainly no one loses hope in the mercy of Allah except the people who disbelieve.", "keywords": ["hope", "hopeful", "future", "positive"]},
    ]
    
    @classmethod
    def load_model(cls):
        if cls.model is None:
            print("Loading embedding model...")
            cls.model = SentenceTransformer("all-MiniLM-L6-v2")
            print("Model loaded")
        return cls.model
    
    @classmethod
    def find_best_verse(cls, user_prompt: str) -> Optional[Dict]:
        """Find best verse: prioritize keyword matches > semantic similarity"""
        cls.load_model()
        
        prompt_vector = cls.model.encode(user_prompt)
        prompt_lower = user_prompt.lower()
        
        keyword_matches = []
        semantic_only = []
        
        for verse in cls.KEY_VERSES:
            verse_vector = cls.model.encode(verse["text_en"])
            sem_sim = np.dot(prompt_vector, verse_vector) / (
                np.linalg.norm(prompt_vector) * np.linalg.norm(verse_vector) + 1e-10
            )
            
            has_keyword = any(kw in prompt_lower for kw in verse.get("keywords", []))
            result = {**verse, "similarity_score": float(sem_sim)}
            
            if has_keyword:
                keyword_matches.append((sem_sim, result))
            else:
                semantic_only.append((sem_sim, result))
        
        # Sort by semantic score
        keyword_matches.sort(key=lambda x: x[0], reverse=True)
        semantic_only.sort(key=lambda x: x[0], reverse=True)
        
        # PRIORITY: keyword match (even with low semantic) > pure semantic (high threshold)
        if keyword_matches and keyword_matches[0][0] > 0.10:
            return keyword_matches[0][1]
        elif semantic_only and semantic_only[0][0] > 0.28:
            return semantic_only[0][1]
        elif keyword_matches:
            return keyword_matches[0][1]
        
        return None
    
    @classmethod
    def is_safe_match(cls, user_prompt: str) -> bool:
        prohibited = ["suicide", "kill", "violence", "haram", "forbidden", "theft"]
        return not any(word in user_prompt.lower() for word in prohibited)
