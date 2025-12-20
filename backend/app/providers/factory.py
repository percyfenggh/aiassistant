from .base import LLMProvider
from .ollama import OllamaProvider
from ..config import settings


def get_provider() -> LLMProvider:
    """
    Factory function to create and return the appropriate LLM provider.

    Returns:
        An instance of the configured LLM provider

    Raises:
        ValueError: If the configured provider is not supported
    """
    provider_name = settings.llm_provider.lower()

    if provider_name == "ollama":
        return OllamaProvider(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
        )
    else:
        raise ValueError(
            f"Unsupported LLM provider: {provider_name}. "
            f"Supported providers: ollama"
        )

