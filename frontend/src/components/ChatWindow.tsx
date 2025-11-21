import { FormEvent, useState } from "react";
import { useChat } from "../hooks/useChat";
import "./ChatWindow.css";

export function ChatWindow() {
  const { messages, sendMessage, isSending, error } = useChat();
  const [input, setInput] = useState("");

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    if (!input.trim()) return;
    void sendMessage(input);
    setInput("");
  };

  return (
    <div className="chat-card">
      <div className="chat-log" role="log" aria-live="polite">
        {messages.map((message) => (
          <article key={message.id} className={`chat-bubble ${message.role}`}>
            <strong>{message.role === "assistant" ? "Assistant" : "You"}</strong>
            <p>{message.content}</p>
          </article>
        ))}
      </div>

      <form className="chat-input" onSubmit={handleSubmit}>
        <label className="sr-only" htmlFor="chat-prompt">
          Prompt
        </label>
        <input
          id="chat-prompt"
          name="prompt"
          placeholder="Ask about your files (once you plug in an LLM)..."
          value={input}
          onChange={(event) => setInput(event.target.value)}
          disabled={isSending}
        />
        <button type="submit" disabled={isSending}>
          {isSending ? "Sending..." : "Send"}
        </button>
      </form>
      {error && <p className="chat-error">{error}</p>}
    </div>
  );
}

