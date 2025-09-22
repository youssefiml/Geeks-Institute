const boardElement = document.getElementById("board");
const messageElement = document.getElementById("message");

let board = Array(9).fill(null);
let player = "X";
let computer = "O";
let level = "easy";
let gameOver = false;

const winCombos = [
  [0,1,2], [3,4,5], [6,7,8],
  [0,3,6], [1,4,7], [2,5,8],
  [0,4,8], [2,4,6]
];

function renderBoard() {
  boardElement.innerHTML = "";
  board.forEach((cell, i) => {
    const div = document.createElement("div");
    div.classList.add("cell");
    div.textContent = cell || "";
    div.onclick = () => makeMove(i);
    boardElement.appendChild(div);
  });
}

function chooseSymbol(symbol) {
  player = symbol;
  computer = symbol === "X" ? "O" : "X";
  restartGame();
}

function setLevel(lvl) {
  level = lvl;
  messageElement.textContent = "Level set to " + lvl;
}

function makeMove(i) {
  if (board[i] || gameOver) return;
  board[i] = player;

  if (checkWinner(player)) {
    messageElement.textContent = "You win!";
    gameOver = true;
    renderBoard();
    return;
  }

  if (board.every(cell => cell)) {
    messageElement.textContent = "Tie game!";
    gameOver = true;
    renderBoard();
    return;
  }

  computerMove();
}

function computerMove() {
  let move;

  if (level === "easy") {
    const emptyCells = board.map((v, i) => v ? null : i).filter(v => v !== null);
    move = emptyCells[Math.floor(Math.random() * emptyCells.length)];
  } else {
    move = bestMove();
  }

  board[move] = computer;

  if (checkWinner(computer)) {
    messageElement.textContent = "Computer wins!";
    gameOver = true;
  } else if (board.every(cell => cell)) {
    messageElement.textContent = "Tie game!";
    gameOver = true;
  }

  renderBoard();
}

function bestMove() {
  // 1. Try to win
  for (let combo of winCombos) {
    const [a, b, c] = combo;
    if (board[a] === computer && board[b] === computer && !board[c]) return c;
    if (board[a] === computer && board[c] === computer && !board[b]) return b;
    if (board[b] === computer && board[c] === computer && !board[a]) return a;
  }

  // 2. Block the player
  for (let combo of winCombos) {
    const [a, b, c] = combo;
    if (board[a] === player && board[b] === player && !board[c]) return c;
    if (board[a] === player && board[c] === player && !board[b]) return b;
    if (board[b] === player && board[c] === player && !board[a]) return a;
  }

  // 3. Random move
  const emptyCells = board.map((v, i) => v ? null : i).filter(v => v !== null);
  return emptyCells[Math.floor(Math.random() * emptyCells.length)];
}

function checkWinner(symbol) {
  return winCombos.some(combo => combo.every(i => board[i] === symbol));
}

function restartGame() {
  board = Array(9).fill(null);
  gameOver = false;
  messageElement.textContent = "";
  renderBoard();
}

renderBoard();
