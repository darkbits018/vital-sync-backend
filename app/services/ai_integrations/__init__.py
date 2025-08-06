from typing import Dict, Any
from app.services.ai_integrations.gemini import GeminiService
from app.services.ai_integrations.mistral import MistralService
from app.services.ai_integrations.huggingface import HuggingFaceService

class AIIntegrationFactory:
    _services = {
        "gemini": GeminiService,
        "mistral": MistralService,
        "huggingface": HuggingFaceService
    }

    @classmethod
    def get_service(cls, model_name: str, api_key: str = None):
        service_class = cls._services.get(model_name.lower())
        if not service_class:
            raise ValueError(f"Unsupported AI model: {model_name}")
        return service_class(api_key=api_key)