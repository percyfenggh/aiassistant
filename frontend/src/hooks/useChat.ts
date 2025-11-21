import { useCallback, useState } from "react";
import { sendChat } from "../lib/api";
import type { ChatMessage } from "../types/chat";

const createMessage = (role: ChatMessage["role"], content: string): ChatMessage => ({
  id: crypto.randomUUID(),
  role,
  content,
});

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    createMessage("assistant", "Hi there! Ask me about the files you'll upload later."),
  ]);
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = useCallback(
    async (content: string) => {
      if (!content.trim()) return;

      const userMessage = createMessage("user", content.trim());
      const nextMessages = [...messages, userMessage];
      setMessages(nextMessages);
      setError(null);
      setIsSending(true);

      try {
        const response = await sendChat(nextMessages);
        setMessages((prev) => [...prev, response.reply]);
      } catch (err) {
        console.error(err);
        setError("Unable to reach the backend. Is it running?");
      } finally {
        setIsSending(false);
      }
    },
    [messages],
  );

  return { messages, sendMessage, isSending, error };
}

