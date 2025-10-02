let player = prompt("Enter your player name:");
let currentEmoji = "";
let options = [];

async function loadGame() {
  const res = await fetch("/game");
  const data = await res.json();
  currentEmoji = data.emoji;
  options = data.options;

  document.getElementById("emoji").textContent = currentEmoji;

  const form = document.getElementById("guessForm");
  form.innerHTML = "";
  options.forEach(opt => {
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
    body: JSON.stringify({ player, guess })
  });

  const result = await res.json();
  document.getElementById("feedback").textContent = result.correct
    ? "Correct!"
    : `Wrong! The correct answer was ${result.answer}`;
  document.getElementById("score").textContent = `Your score: ${result.score}`;

  loadLeaderboard();
  loadGame();
});

async function loadLeaderboard() {
  const res = await fetch("/leaderboard");
  const data = await res.json();
  const list = document.getElementById("leaderboard");
  list.innerHTML = "";
  data.forEach(p => {
    list.innerHTML += `<li>${p.name}: ${p.score}</li>`;
  });
}

loadGame();
