import { useState } from "react";
import ReactMarkdown from "react-markdown";
import { FaGithub, FaLinkedin } from "react-icons/fa";
import API from "./api";
import "./index.css";

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim()) return;

    let userMsg = {
      role: "user",
      text: question,
    };

    setMessages((prev) => [...prev, userMsg]);

    setQuestion("");
    setLoading(true);

    try {
      const res = await API.post("/chat", {
        question: userMsg.text,
      });

      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text: res.data.answer,
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text: "Server error. Try again.",
        },
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="app">
      <nav>
        <div className="logo">⚡ GateGPT</div>

        <div>
          <a href="/about.html">About</a>
          <a href="https://github.com/tomx-1101/gate_material" target="_blank" rel="noopener noreferrer">
            Resources
          </a>
        </div>
      </nav>

      <main>
        <section className="hero">
          <h1>
            Your Personal
            <br />
            <span>GATE CSE AI Tutor</span>
          </h1>

          <p>
            An intelligent multi-agent RAG assistant powered by Gemini AI, designed to help GATE CSE aspirants using trusted books, notes, solved papers, and previous year questions.
          </p>

          <div className="stats">
            <div>📚 2800+ Pages</div>
            <div>📝 PYQs Included</div>
            <div>🤖 Gemini Powered</div>
          </div>

          <div className="links">
            <a
              href="https://github.com/tomx-1101/gate_meterial"
              target="_blank"
              rel="noopener noreferrer"
            >
              <button>Study Material</button>
            </a>

            <a
              href="https://github.com/tomx-1101/gate_meterial"
              target="_blank"
              rel="noopener noreferrer"
            >
              <button>Source Code</button>
            </a>
          </div>
        </section>

        <section className="chat-card">
          <div className="chat-header">🤖 Assistant Online</div>

          <div className="chat-box">
            {messages.length === 0 && (
              <div className="welcome">Ask me OS, DBMS, CN, DSA doubts 🚀</div>
            )}

            {messages.map((m, i) => (
              <div
                key={i}
                className={m.role === "user" ? "user-message" : "ai-message"}
              >
                <ReactMarkdown>{m.text}</ReactMarkdown>
              </div>
            ))}

            {loading && <p className="thinking">AI is thinking...</p>}
          </div>

          <div className="input-area">
            <input
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  askQuestion();
                }
              }}
              placeholder="Ask your GATE doubt..."
            />

            <button onClick={askQuestion}>➤</button>
          </div>
        </section>
      </main>

      <footer>
        <p>Built by Sajid Saleem</p>

        <div>
          <a href="https://github.com/Sajid-1101" target="_blank" rel="noopener noreferrer">
            <FaGithub />
          </a>

          <a href="https://www.linkedin.com/in/sajid-saleem-5742433b2/" target="_blank" rel="noopener noreferrer">
            <FaLinkedin />
          </a>
        </div>
      </footer>
    </div>
  );
}

export default App;
