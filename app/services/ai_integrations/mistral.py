import requests
from typing import Dict, Any


class MistralService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.base_url = "https://api.mistral.ai/v1/chat/completions "

    def generate_response(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "mistral-small-latest",
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(self.base_url, headers=headers, json=payload)
        return response.json()['choices'][0]['message']['content']

    def extract_preferences(self, message: str) -> Dict[str, Any]:
        prompt = f"""
        Analyze the following message and extract any health-related preferences:

        "{message}"

        Return a JSON object with keys like:
        - goal
        - activity_level
        - dietary_restrictions
        - preferred_foods
        - disliked_foods
        - workout_frequency
        """
        response = self.generate_response(prompt)
        return self._parse_ai_response(response)

    def _parse_ai_response(self, text: str) -> Dict[str, Any]:
        # Add logic to parse and validate JSON from AI
        return {
            "raw_response": text,
            "preferences": {}  # Replace with real parsing
        }