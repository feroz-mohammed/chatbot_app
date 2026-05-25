let conversationId = Number(localStorage.getItem("conversationId") || "") || null;
const chatWindow = document.getElementById("chatWindow");
const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const newChatBtn = document.getElementById("newChatBtn");

function addMessage(role, content) {
  const div = document.createElement("div");
  div.className = `msg ${role}`;
  div.textContent = content;
  chatWindow.appendChild(div);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function setThinking(isThinking) {
  if (isThinking) {
    const div = document.createElement("div");
    div.id = "thinking";
    div.className = "msg assistant thinking";
    div.textContent = "Thinking...";
    chatWindow.appendChild(div);
    chatWindow.scrollTop = chatWindow.scrollHeight;
  } else {
    const el = document.getElementById("thinking");
    if (el) el.remove();
  }
}

async function sendMessage(text) {
  try {
    setThinking(true);
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: text,
        conversation_id: conversationId,
        user_id: null,
      }),
    });
    const data = await res.json();
    setThinking(false);
    if (!res.ok) throw new Error(data.detail || "Request failed");
    conversationId = data.conversation_id;
    localStorage.setItem("conversationId", String(conversationId));
    addMessage("assistant", data.reply);
  } catch (e) {
    setThinking(false);
    addMessage("assistant", "Error: " + e.message);
  }
}

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = messageInput.value.trim();
  if (!text) return;
  addMessage("user", text);
  messageInput.value = "";
  messageInput.focus();
  await sendMessage(text);
});

newChatBtn.addEventListener("click", () => {
  conversationId = null;
  localStorage.removeItem("conversationId");
  chatWindow.innerHTML = "";
});

// Restore history if we already have a conversation id
async function loadHistory() {
  if (!conversationId) return;
  try {
    const res = await fetch(`/api/conversations/${conversationId}/messages`);
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Failed to load history");
    chatWindow.innerHTML = "";
    for (const m of data.messages) {
      if (m.role === "system") continue;
      addMessage(m.role, m.content);
    }
  } catch (e) {
    console.warn(e);
  }
}
loadHistory();
