import express from "express";
import path from "path";
import { fileURLToPath } from "url";

const app = express();
const PORT = 3000;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

app.use(express.json());
app.use(express.static(__dirname + "/public"));

const emojis = [
  { emoji: "😀", name: "smile" },
  { emoji: "🐱", name: "cat" },
  { emoji: "🍕", name: "pizza" },
  { emoji: "🚗", name: "car" },
  { emoji: "🏀", name: "basketball" },
  { emoji: "🎵", name: "music" },
  { emoji: "🌍", name: "earth" },
  { emoji: "💻", name: "computer" },
  { emoji: "📚", name: "books" },
  { emoji: "✈️", name: "airplane" },
  { emoji: "⚽", name: "soccer" },
  { emoji: "🎮", name: "video game" },
  { emoji: "🌳", name: "tree" },
  { emoji: "🌟", name: "star" },
  { emoji: "🌊", name: "ocean" },
  { emoji: "🌈", name: "rainbow" },
];

let leaderboard = [];

function getRandomQuestion() {
  const correct = emojis[Math.floor(Math.random() * emojis.length)];

  const distractors = emojis
    .filter(e => e.name !== correct.name)
    .sort(() => 0.5 - Math.random())
    .slice(0, 3);

  const options = [...distractors.map(e => e.name), correct.name]
    .sort(() => 0.5 - Math.random());

  return { emoji: correct.emoji, answer: correct.name, options };
}

let currentQuestion = getRandomQuestion();
let scores = {};

app.get("/game", (req, res) => {
  currentQuestion = getRandomQuestion();
  res.json({
    emoji: currentQuestion.emoji,
    options: currentQuestion.options,
  });
});

app.post("/guess", (req, res) => {
  const { player, guess } = req.body;

  if (!scores[player]) scores[player] = 0;

  let correct = guess === currentQuestion.answer;
  if (correct) {
    scores[player] += 1;
  }

  leaderboard = Object.entries(scores)
    .map(([name, score]) => ({ name, score }))
    .sort((a, b) => b.score - a.score)
    .slice(0, 5);

  res.json({
    correct,
    answer: currentQuestion.answer,
    score: scores[player],
  });
});

app.get("/leaderboard", (req, res) => {
  res.json(leaderboard);
});

app.listen(PORT, () =>
  console.log(`🚀 Emoji Game running on http://localhost:${PORT}`)
);