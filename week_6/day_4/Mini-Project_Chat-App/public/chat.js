const socket = io();

const entry = document.getElementById("entry");
const usernameInput = document.getElementById("username");
const roomInput = document.getElementById("room");
const joinBtn = document.getElementById("joinBtn");

const chatScreen = document.getElementById("chatScreen");
const roomNameEl = document.getElementById("roomName");
const hdrRoom = document.getElementById("hdrRoom");
const usersList = document.getElementById("usersList");
const messagesEl = document.getElementById("messages");
const msgInput = document.getElementById("msgInput");
const sendBtn = document.getElementById("sendBtn");
const leaveBtn = document.getElementById("leaveBtn");
const typingEl = document.getElementById("typing");

let currentRoom = null;
let currentUser = null;
let focused = true;
let origTitle = document.title;
let notifTimer = null;

window.addEventListener("focus", () => {
  focused = true;
  document.title = origTitle;
  if (notifTimer) {
    clearInterval(notifTimer);
    notifTimer = null;
  }
});

window.addEventListener("blur", () => (focused = false));

function el(tag, cls) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  return e;
}

function appendMessage(m) {
  const row = el("div", "msg");
  const time = new Date(m.ts).toLocaleTimeString();

  if (m.system) {
    row.classList.add("system");
    row.textContent = `${m.text} — ${time}`;
  } else {
    const author = el("div", "msg-author");
    author.textContent = m.username;

    const body = el("div", "msg-body");
    body.textContent = m.text;

    const meta = el("div", "msg-meta");
    meta.textContent = time;

    row.appendChild(author);
    row.appendChild(body);
    row.appendChild(meta);
  }

  messagesEl.appendChild(row);
  messagesEl.scrollTop = messagesEl.scrollHeight;

  if (!focused && !m.system && m.username !== currentUser) {
    notifyNewMessage(m);
  }
}

function notifyNewMessage(m) {
  // sound beep
  try {
    const audio = new Audio(
      "data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEAQB8AAIA+AAACABAAZGF0YQAAAAA="
    );
    audio.play().catch(() => {});
  } catch (e) {}

  let visible = true;
  document.title = `Nouveau message • ${m.username}`;

  if (notifTimer) clearInterval(notifTimer);

  notifTimer = setInterval(() => {
    document.title = visible ? `• Nouveau message` : origTitle;
    visible = !visible;
  }, 1200);
}

joinBtn.addEventListener("click", () => {
  const username = usernameInput.value.trim() || "Anon";
  const room = roomInput.value.trim() || "general";

  currentUser = username;
  currentRoom = room;

  socket.emit("joinRoom", { username, room });
  entry.classList.add("hidden");
  chatScreen.classList.remove("hidden");

  roomNameEl.textContent = room;
  hdrRoom.textContent = `Salle: ${room}`;
  messagesEl.innerHTML = "";
});

sendBtn.addEventListener("click", sendMessage);

msgInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    sendMessage();
  }
  socket.emit("typing", { room: currentRoom, typing: true });
  setTimeout(() => socket.emit("typing", { room: currentRoom, typing: false }), 700);
});

function sendMessage() {
  const text = msgInput.value.trim();
  if (!text) return;
  socket.emit("chatMessage", { room: currentRoom, text });
  msgInput.value = "";
}

leaveBtn.addEventListener("click", () => {
  location.reload();
});

socket.on("roomHistory", (history) => {
  messagesEl.innerHTML = "";
  history.forEach((m) => appendMessage(m));
});

socket.on("message", (m) => {
  appendMessage(m);
});

socket.on("roomUsers", ({ users }) => {
  usersList.innerHTML = "";
  users.forEach((u) => {
    const li = el("li");
    li.textContent = u;
    usersList.appendChild(li);
  });
});

socket.on("typing", ({ username, typing }) => {
  typingEl.textContent = typing ? `${username} est en train d'écrire...` : "";
});