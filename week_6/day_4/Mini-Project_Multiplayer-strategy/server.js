import express from 'express';
import bodyParser from 'body-parser';
import cors from 'cors';
import { v4 as uuidv4 } from 'uuid';

const app = express();

app.use(cors());
app.use(bodyParser.json());
app.use(express.static('public'));

const users = {};
const games = {};
const GRID_SIZE = 10;

function createEmptyGrid() {
  return Array.from({ length: GRID_SIZE }, () => Array(GRID_SIZE).fill(0));
}

function createGame(playerA, playerB = null) {
  const id = uuidv4();
  const grid = createEmptyGrid();

  const obstacles = [
    [2, 2], [2, 3], [3, 2],
    [6, 6], [6, 5], [5, 6], [4, 7]
  ];

  obstacles.forEach(([r, c]) => {
    if (r >= 0 && r < GRID_SIZE && c >= 0 && c < GRID_SIZE) grid[r][c] = 1;
  });

  const baseA = { r: 0, c: 0 };
  const baseB = { r: GRID_SIZE - 1, c: GRID_SIZE - 1 };

  const game = {
    id,
    grid,
    baseA,
    baseB,
    players: {
      A: { username: playerA, pos: { ...baseA }, connected: true },
      B: playerB ? { username: playerB, pos: { ...baseB }, connected: !!playerB } : null,
    },
    turn: 'A',
    winner: null,
  };

  games[id] = game;
  return game;
}

function isValidMove(game, from, to) {
  if (to.r < 0 || to.r >= GRID_SIZE || to.c < 0 || to.c >= GRID_SIZE) return false;

  const dr = Math.abs(from.r - to.r);
  const dc = Math.abs(from.c - to.c);

  if (!((dr === 1 && dc === 0) || (dr === 0 && dc === 1))) return false;
  if (game.grid[to.r][to.c] === 1) return false;

  const otherPos = game.players.A && game.players.B
    ? (from === game.players.A.pos ? game.players.B.pos : game.players.A.pos)
    : null;

  if (otherPos && to.r === otherPos.r && to.c === otherPos.c) return false;

  return true;
}

function checkAttackOrWin(game, playerKey) {
  const player = game.players[playerKey];
  const enemyBase = playerKey === 'A' ? game.baseB : game.baseA;

  if (player.pos.r === enemyBase.r && player.pos.c === enemyBase.c) {
    game.winner = playerKey;
    return { type: 'win', winner: playerKey };
  }

  const dr = Math.abs(player.pos.r - enemyBase.r);
  const dc = Math.abs(player.pos.c - enemyBase.c);

  if ((dr === 1 && dc === 0) || (dr === 0 && dc === 1)) {
    game.winner = playerKey;
    return { type: 'attack-win', winner: playerKey };
  }

  return { type: 'none' };
}

app.post('/api/register', (req, res) => {
  const { username, password } = req.body;
  if (!username || !password) return res.status(400).json({ error: 'username and password required' });
  if (users[username]) return res.status(400).json({ error: 'username taken' });
  users[username] = { password };
  res.json({ ok: true });
});

app.post('/api/login', (req, res) => {
  const { username, password } = req.body;
  if (!users[username] || users[username].password !== password)
    return res.status(401).json({ error: 'invalid credentials' });
  res.json({ ok: true });
});

app.post('/api/start', (req, res) => {
  const { username, opponent } = req.body;
  if (!username) return res.status(400).json({ error: 'username required' });
  const game = createGame(username, opponent || null);
  res.json({ gameId: game.id, game });
});

app.post('/api/join', (req, res) => {
  const { username, gameId } = req.body;
  const game = games[gameId];
  if (!game) return res.status(404).json({ error: 'game not found' });
  if (game.players.B) return res.status(400).json({ error: 'game already has second player' });

  game.players.B = { username, pos: { ...game.baseB }, connected: true };
  res.json({ ok: true, game });
});

app.get('/api/game/:id', (req, res) => {
  const game = games[req.params.id];
  if (!game) return res.status(404).json({ error: 'game not found' });
  res.json({ game });
});

app.post('/api/move', (req, res) => {
  const { gameId, playerKey, to } = req.body;
  const game = games[gameId];
  if (!game) return res.status(404).json({ error: 'game not found' });
  if (game.winner) return res.status(400).json({ error: 'game finished', winner: game.winner });
  if (game.turn !== playerKey) return res.status(400).json({ error: "not player's turn" });

  const player = game.players[playerKey];
  if (!isValidMove(game, player.pos, to)) return res.status(400).json({ error: 'invalid move' });

  player.pos = { r: to.r, c: to.c };
  const result = checkAttackOrWin(game, playerKey);
  game.turn = game.turn === 'A' ? 'B' : 'A';

  res.json({ ok: true, result, game });
});

app.get('/api/games', (req, res) => {
  res.json({ games: Object.values(games).map(g => ({ id: g.id, players: g.players, winner: g.winner })) });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`✅ Server running on port ${PORT}`));
