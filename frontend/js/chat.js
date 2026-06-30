/* InfraGuidAI — Chat Controller */

// Auth guard
if (!AuthManager.guardPage()) {
  throw new Error("Not authenticated");
}

// Show admin link if user is admin
if (AuthManager.isAdmin()) {
  const adminLink = document.getElementById("adminLink");
  if (adminLink) adminLink.style.display = "";
}

// Render user block in sidebar
AuthManager.renderUserBlock(document.getElementById("userBlock"));

// DOM references
const healthStatus = document.getElementById("healthStatus");
const messages = document.getElementById("messages");
const sources = document.getElementById("sources");
const form = document.getElementById("chatForm");
const input = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const alertBox = document.getElementById("alert");
let sessionId = localStorage.getItem("infraguid_session_id");

function showAlert(message) {
  alertBox.textContent = message;
  alertBox.hidden = !message;
}

function setHealth(ok, text) {
  healthStatus.textContent = text;
  healthStatus.className = `status-pill ${ok ? "ok" : "fail"}`;
}

async function checkHealth() {
  try {
    const response = await fetch("/api/health");
    setHealth(response.ok, response.ok ? "Healthy" : "Unhealthy");
  } catch {
    setHealth(false, "Offline");
  }
}

// Render assistant content with fenced code blocks (```), inline `code` and
// **bold**. Returns trusted HTML built from escaped fragments only.
function renderRichContent(text) {
  const parts = String(text).split(/```/);
  let html = "";
  parts.forEach((part, index) => {
    if (index % 2 === 1) {
      // Code fence: first line may be a language hint
      const newline = part.indexOf("\n");
      let lang = "";
      let code = part;
      if (newline !== -1) {
        const firstLine = part.slice(0, newline).trim();
        if (firstLine && !firstLine.includes(" ")) {
          lang = firstLine;
          code = part.slice(newline + 1);
        }
      }
      code = code.replace(/\n$/, "");
      html += `<div class="code-block"><div class="code-block-head"><span>${escapeHtml(lang || "code")}</span><button class="copy-btn" type="button">Copy</button></div><pre><code>${escapeHtml(code)}</code></pre></div>`;
    } else {
      let safe = escapeHtml(part);
      safe = safe.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
      safe = safe.replace(/`([^`]+)`/g, "<code>$1</code>");
      html += safe;
    }
  });
  return html;
}

function addMessage(role, content, meta = "") {
  // Remove welcome state if present
  const welcome = document.querySelector(".welcome-state");
  if (welcome) welcome.remove();

  const wrapper = document.createElement("div");
  wrapper.className = `message ${role}`;
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  if (role === "assistant") {
    bubble.innerHTML = renderRichContent(content);
    bubble.querySelectorAll(".copy-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const code = btn.closest(".code-block").querySelector("code").textContent;
        navigator.clipboard.writeText(code).then(() => {
          btn.textContent = "Copied";
          btn.classList.add("copied");
          setTimeout(() => { btn.textContent = "Copy"; btn.classList.remove("copied"); }, 1500);
        });
      });
    });
  } else {
    bubble.textContent = content;
  }
  wrapper.appendChild(bubble);
  if (meta && meta !== "pending") {
    const metaNode = document.createElement("div");
    metaNode.className = "meta";
    metaNode.textContent = meta;
    wrapper.appendChild(metaNode);
  }
  messages.appendChild(wrapper);
  messages.scrollTop = messages.scrollHeight;
}

function addTypingIndicator() {
  const wrapper = document.createElement("div");
  wrapper.className = "message assistant";
  wrapper.id = "typingIndicator";
  const indicator = document.createElement("div");
  indicator.className = "typing-indicator";
  indicator.innerHTML = "<span></span><span></span><span></span>";
  wrapper.appendChild(indicator);
  messages.appendChild(wrapper);
  messages.scrollTop = messages.scrollHeight;
}

function removeTypingIndicator() {
  const el = document.getElementById("typingIndicator");
  if (el) el.remove();
}

function renderSources(items) {
  sources.innerHTML = "";
  if (!items || items.length === 0) {
    sources.innerHTML = '<div style="color:var(--text-muted);font-size:12px;">No sources returned yet.</div>';
    return;
  }
  for (const item of items) {
    const node = document.createElement("div");
    node.className = "source";
    node.innerHTML = `<strong>${escapeHtml(item.title || "Untitled")}</strong>
      <a href="/api/documents/${encodeURIComponent(item.path || "")}" target="_blank" class="source-link" title="View Source">
        <svg width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" style="display:inline;vertical-align:-1px;margin-right:4px;"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
        ${escapeHtml(item.path || "")}
      </a>`;
    sources.appendChild(node);
  }
}

async function sendMessage(message) {
  sendButton.disabled = true;
  showAlert("");
  addMessage("user", message);
  addTypingIndicator();
  try {
    const data = await AuthManager.safeFetchJson("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, session_id: sessionId }),
    });

    removeTypingIndicator();
    sessionId = data.session_id;
    localStorage.setItem("infraguid_session_id", sessionId);
    addMessage("assistant", data.answer);
    renderSources(data.sources);
  } catch (error) {
    removeTypingIndicator();
    showAlert(error.message);
  } finally {
    sendButton.disabled = false;
    input.focus();
  }
}

// Auto-resize textarea
input.addEventListener("input", () => {
  input.style.height = "auto";
  input.style.height = Math.min(input.scrollHeight, 160) + "px";
});

// Handle enter key (shift+enter for newline)
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    form.dispatchEvent(new Event("submit"));
  }
});

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const message = input.value.trim();
  if (!message) return;
  input.value = "";
  input.style.height = "auto";
  sendMessage(message);
});

document.querySelectorAll("[data-prompt]").forEach((button) => {
  button.addEventListener("click", () => {
    input.value = button.dataset.prompt;
    input.focus();
  });
});

// Welcome state
const user = AuthManager.getUser();
messages.innerHTML = `
  <div class="welcome-state">
    <div class="welcome-icon">
      <svg width="32" height="32" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
    </div>
    <h2>Welcome, ${escapeHtml(user ? user.name.split(" ")[0] : "User")}</h2>
    <p>InfraGuidAI is ready. Search standards, generate infrastructure code, or query incident runbooks.</p>
  </div>
`;

renderSources([]);
checkHealth();
setInterval(checkHealth, 30000);
