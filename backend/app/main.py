from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Literal


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


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Placeholder chat endpoint. Echoes the last user message and can be replaced
    with real model integration later on.
    """
    fallback = "Hello! I'm not connected to a model yet, but I'm ready when you are."
    last_user_message = next(
        (msg.content for msg in reversed(request.messages) if msg.role == "user"),
        None,
    )

    reply_text = (
        f"You said: {last_user_message}"
        if last_user_message
        else fallback
    )

    reply = ChatMessage(role="assistant", content=reply_text)
    return ChatResponse(reply=reply)

