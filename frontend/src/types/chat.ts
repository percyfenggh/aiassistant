export type Role = "user" | "assistant";

export interface ChatMessage {
  role: Role;
  content: string;
  id: string;
}

export interface ChatTurn {
  user: ChatMessage;
  assistant?: ChatMessage;
}

