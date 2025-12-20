from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Literal

from .providers import get_provider
from .providers.base import LLMProvider


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]


class ChatResponse(BaseModel):
    reply: ChatMessage


app = FastAPI(title="AI Chat Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM provider
try:
    provider: LLMProvider = get_provider()
except Exception:
    provider = None


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat endpoint that sends messages to the configured LLM provider.
    """
    if not request.messages:
        raise HTTPException(
            status_code=400, detail="At least one message is required"
        )

    if provider is None:
        raise HTTPException(
            status_code=500,
            detail="LLM provider not initialized",
        )

    try:
        reply_text = await provider.chat(request.messages)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get response from LLM provider: {str(e)}",
        )

    reply = ChatMessage(role="assistant", content=reply_text)
    return ChatResponse(reply=reply)

