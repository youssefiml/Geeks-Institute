let player = prompt("Enter your player name:");
let currentEmoji = "";
let options = [];
const errorElement = document.querySelector(".error");

if (!player) {
  player = "guest";
}

async function loadGame() {
  const res = await fetch("/game");
  const data = await res.json();
  currentEmoji = data.emoji;
  options = data.options;

  document.getElementById("emoji").textContent = currentEmoji;

  const form = document.getElementById("guessForm");
  form.innerHTML = "";
  options.forEach((opt) => {
    form.innerHTML += `
      <label>
        <input type="radio" name="guess" value="${opt}" required>
        ${opt}
      </label><br>
    `;
  });
}

document.getElementById("submitBtn").addEventListener("click", async (e) => {
  e.preventDefault();
  const formData = new FormData(document.getElementById("guessForm"));
  const guess = formData.get("guess");

  const res = await fetch("/guess", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ player, guess }),
  });
  errorElement.style.display = "none";

  const result = await res.json();
  if (!guess) {
    errorElement.style.display = "block";
    errorElement.textContent = "Please select an option.";
    return;
  }

  loadLeaderboard();
  loadGame();
});

async function loadLeaderboard() {
  const res = await fetch("/leaderboard");
  const data = await res.json();
  const list = document.getElementById("leaderboard");
  list.innerHTML = "";
  data.forEach((p) => {
    list.innerHTML += `<li>${p.name}: ${p.score}</li>`;
  });
}

loadGame();
