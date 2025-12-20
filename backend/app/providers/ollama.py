import httpx
from typing import TYPE_CHECKING, List

from .base import LLMProvider

if TYPE_CHECKING:
    from ..main import ChatMessage


class OllamaProvider(LLMProvider):
    """Provider for Ollama local/remote models."""

    def __init__(self, base_url: str, model: str):
        """
        Initialize Ollama provider.

        Args:
            base_url: Base URL for Ollama API (e.g., http://localhost:11434)
            model: Model name to use (e.g., llama2, mistral, etc.)
        """
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.client = httpx.AsyncClient(timeout=60.0)

    async def chat(self, messages: List["ChatMessage"]) -> str:
        """
        Send chat messages to Ollama and return the response.

        Args:
            messages: List of chat messages with role and content

        Returns:
            The assistant's response as a string

        Raises:
            Exception: If the request to Ollama fails with detailed error message
        """
        # Convert ChatMessage objects to Ollama format
        ollama_messages = [
            {"role": msg.role, "content": msg.content} for msg in messages
        ]

        payload = {
            "model": self.model,
            "messages": ollama_messages,
            "stream": False,
        }

        try:
            response = await self.client.post(
                f"{self.base_url}/api/chat",
                json=payload,
            )
            response.raise_for_status()
            result = response.json()
            return result.get("message", {}).get("content", "")
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code if hasattr(e, "response") else None
            if status_code == 404:
                error_msg = (
                    f"Ollama returned 404 Not Found. This usually means:\n"
                    f"  - The model '{self.model}' is not available on your Ollama instance\n"
                    f"  - Ollama is not running at {self.base_url}\n"
                    f"  - The API endpoint is incorrect\n\n"
                    f"To fix:\n"
                    f"  1. Check if Ollama is running: curl {self.base_url}/api/tags\n"
                    f"  2. List available models: ollama list\n"
                    f"  3. Set the correct model via OLLAMA_MODEL environment variable (e.g., OLLAMA_MODEL=llama3:8b)"
                )
            elif status_code == 500:
                error_msg = (
                    f"Ollama returned 500 Internal Server Error. This usually means:\n"
                    f"  - The model '{self.model}' exists but failed to load or respond\n"
                    f"  - There's an issue with the Ollama server\n\n"
                    f"To fix:\n"
                    f"  1. Check Ollama logs for errors\n"
                    f"  2. Try pulling the model: ollama pull {self.model}\n"
                    f"  3. Restart Ollama service"
                )
            elif status_code is not None:
                error_msg = (
                    f"Ollama returned HTTP {status_code}. "
                    f"Request to {self.base_url}/api/chat failed. "
                    f"Error: {str(e)}"
                )
            else:
                error_msg = f"Failed to communicate with Ollama: {str(e)}"
            
            raise Exception(error_msg)
        except httpx.RequestError as e:
            error_msg = (
                f"Failed to connect to Ollama at {self.base_url}. "
                f"This usually means Ollama is not running or not accessible.\n\n"
                f"To fix:\n"
                f"  1. Ensure Ollama is running: ollama serve\n"
                f"  2. Check if the base URL is correct (current: {self.base_url})\n"
                f"  3. For remote Ollama, verify network connectivity"
            )
            raise Exception(error_msg)
        except httpx.HTTPError as e:
            raise Exception(f"Failed to communicate with Ollama: {str(e)}")
        except KeyError as e:
            raise Exception(f"Unexpected response format from Ollama: {str(e)}")

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
