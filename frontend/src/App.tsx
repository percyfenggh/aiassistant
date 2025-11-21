import { ChatWindow } from "./components/ChatWindow";
import "./App.css";

function App() {
  return (
    <main className="app-shell">
      <section className="app-card">
        <header>
          <p className="eyebrow">FastAPI · React</p>
          <h1>AI Chat Playground</h1>
          <p className="lede">
            Use this starter to plug in your own LLM or hosted API later. The UI
            already streams messages to the backend and renders Assistant
            replies.
          </p>
        </header>
        <ChatWindow />
      </section>
    </main>
  );
}

export default App;

