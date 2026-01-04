import httpx
import json
from app.config import settings
from typing import Dict, List, Optional

class DeepseekService:
    """Service to interact with Deepseek API for understanding user prompts"""
    
    def __init__(self):
        self.api_key = settings.deepseek_api_key
        self.base_url = settings.deepseek_api_base_url
        # Use sync client by default since we need to call this from sync contexts too
        self.client = httpx.Client(headers={"Authorization": f"Bearer {self.api_key}"})
        # Also have an async client available
        self.async_client = httpx.AsyncClient(headers={"Authorization": f"Bearer {self.api_key}"})
    
    def _detect_language(self, text: str) -> str:
        """Detect if text is Arabic or English"""
        # Simple heuristic: check for Arabic Unicode ranges
        arabic_count = sum(1 for char in text if '\u0600' <= char <= '\u06FF')
        english_count = sum(1 for char in text if char.isalpha() and ord(char) < 128)
        
        if arabic_count > english_count:
            return "ar"
        return "en"
    
    async def analyze_prompt(self, user_prompt: str) -> Dict:
        """
        Use Deepseek to analyze user prompt and extract relevant topics/keywords
        Supports both English and Arabic prompts
        Returns: {
            "topics": ["patience", "guidance"],
            "keywords": ["struggling", "difficult times"],
            "emotion": "distressed",
            "summary": "User seeking guidance on handling difficulties with patience",
            "prompt_language": "en"
        }
        """
        try:
            prompt_language = self._detect_language(user_prompt)
            
            analysis_prompt = f"""Analyze this user prompt about a problem they're facing during Ramadan and extract:
1. Main topics/themes (e.g., patience, forgiveness, guidance, family, health, faith, wealth, relationships, etc.)
2. Key emotional state or sentiment
3. A concise summary of their problem
4. Keywords that can help find relevant Quran verses or hadiths

User prompt: "{user_prompt}"

Return as JSON with keys: topics (list), keywords (list), emotion (string), summary (string)"""
            
            response = await self._call_deepseek_api(analysis_prompt)
            
            # Parse the response
            try:
                result = json.loads(response)
                result["prompt_language"] = prompt_language
                return result
            except json.JSONDecodeError:
                # If response is not JSON, try to extract it
                return {
                    "topics": [],
                    "keywords": user_prompt.split(),
                    "emotion": "neutral",
                    "summary": user_prompt,
                    "prompt_language": prompt_language
                }
                
        except Exception as e:
            print(f"Error analyzing prompt with Deepseek: {e}")
            # Fallback: return basic analysis
            return {
                "topics": [],
                "keywords": user_prompt.split(),
                "emotion": "neutral",
                "summary": user_prompt,
                "prompt_language": self._detect_language(user_prompt)
            }
    
    async def generate_explanation(
        self,
        user_prompt: str,
        verse_or_hadith_text: str,
        item_type: str = "verse"
    ) -> Dict[str, str]:
        """
        Generate explanation for why a specific verse/hadith was chosen
        Returns both English and Arabic explanations
        """
        try:
            explanation_prompt = f"""The user asked: "{user_prompt}"

A relevant {item_type} was found: "{verse_or_hadith_text}"

Provide a brief explanation (2-3 sentences) in both English and Arabic for why this {item_type} is relevant to address the user's concern. 
Focus on the connection between the user's problem and the wisdom in this {item_type}.

Return as JSON with keys: explanation_english (string), explanation_arabic (string)"""
            
            response = await self._call_deepseek_api(explanation_prompt)
            
            try:
                result = json.loads(response)
                return {
                    "explanation_english": result.get("explanation_english", ""),
                    "explanation_arabic": result.get("explanation_arabic", "")
                }
            except json.JSONDecodeError:
                return {
                    "explanation_english": "This content addresses your concern.",
                    "explanation_arabic": "هذا المحتوى يتناول مخاوفك."
                }
                
        except Exception as e:
            print(f"Error generating explanation: {e}")
            return {
                "explanation_english": "Relevant guidance for your situation.",
                "explanation_arabic": "إرشادات ذات صلة لحالتك."
            }
    
    async def _call_deepseek_api(self, prompt: str) -> str:
        """Call the Deepseek API with the given prompt"""
        try:
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            response = await self.async_client.post(
                f"{self.base_url}/chat/completions",
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get("choices", [{}])[0].get("message", {}).get("content", "")
        except Exception as e:
            print(f"Error calling Deepseek API: {e}")
            raise
    
    def _call_deepseek_api_sync(self, prompt: str) -> str:
        """Call the Deepseek API synchronously with the given prompt"""
        try:
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            response = self.client.post(
                f"{self.base_url}/chat/completions",
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get("choices", [{}])[0].get("message", {}).get("content", "")
        except Exception as e:
            print(f"Error calling Deepseek API: {e}")
            raise
