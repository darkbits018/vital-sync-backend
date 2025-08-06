from google.generativeai import GenerativeModel, configure
from typing import Dict, Any


class GeminiService:
    def __init__(self, api_key: str = None):
        if api_key:
            configure(api_key=api_key)
        self.model = GenerativeModel("gemini-2.0-flash")

    def generate_response(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text

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
        response = self.model.generate_content(prompt)
        return self._parse_ai_response(response.text)

    def _parse_ai_response(self, text: str) -> Dict[str, Any]:
        # Add logic to parse and validate JSON from AI
        return {
            "raw_response": text,
            "preferences": {}  # Replace with real parsing
        }