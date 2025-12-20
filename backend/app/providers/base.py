from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ..main import ChatMessage


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    async def chat(self, messages: List["ChatMessage"]) -> str:
        """
        Send chat messages to the LLM provider and return the response.

        Args:
            messages: List of chat messages with role and content

        Returns:
            The assistant's response as a string

        Raises:
            Exception: If the provider request fails
        """
        pass

