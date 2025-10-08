let state = null;
let myUsername = null;
let myPlayerKey = null;
let currentGameId = null;
const boardEl = document.getElementById('board');
const infoEl = document.getElementById('info');
function renderBoard(game) {
  boardEl.innerHTML = '';
  for (let r = 0; r < 10; r++) {
    for (let c = 0; c < 10; c++) {
      const cell = document.createElement('div');
      cell.className = 'cell';

      const val = game.grid[r][c];
      if (val === 1) cell.classList.add('obstacle');

      if (game.baseA.r === r && game.baseA.c === c) cell.classList.add('baseA');
      if (game.baseB.r === r && game.baseB.c === c) cell.classList.add('baseB');

      if (game.players.A && game.players.A.pos.r === r && game.players.A.pos.c === c)
        cell.classList.add('playerA');
      if (game.players.B && game.players.B.pos.r === r && game.players.B.pos.c === c)
        cell.classList.add('playerB');

      let text = '';
      if (cell.classList.contains('playerA')) text = 'A';
      if (cell.classList.contains('playerB')) text = 'B';
      if (cell.classList.contains('baseA')) text = text ? text : 'BA';
      if (cell.classList.contains('baseB')) text = text ? text : 'BB';
      cell.textContent = text;

      boardEl.appendChild(cell);
    }
  }
}
async function api(path, method = 'GET', body) {
  const res = await fetch('/api' + path, {
    method,
    headers: body ? { 'Content-Type': 'application/json' } : undefined,
    body: body ? JSON.stringify(body) : undefined,
  });
  return res.json();
}
document.getElementById('start').addEventListener('click', async () => {
  const username = document.getElementById('username').value.trim();
  if (!username) return alert('username needed');
  myUsername = username;
  const { gameId, game } = await api('/start', 'POST', { username });
  currentGameId = gameId;
  myPlayerKey = 'A';
  state = game;
  renderBoard(game);
  showInfo(game);
});

document.getElementById('join').addEventListener('click', async () => {
  const username = document.getElementById('username').value.trim();
  const gameId = document.getElementById('gameIdInput').value.trim();
  if (!username || !gameId) return alert('username and game id required');
  myUsername = username;
  const res = await api('/join', 'POST', { username, gameId });
  if (res.error) return alert(res.error);
  currentGameId = gameId;
  myPlayerKey = 'B';
  state = res.game;
  renderBoard(state);
  showInfo(state);
});
async function refresh() {
  if (!currentGameId) return;
  const res = await api('/game/' + currentGameId);
  if (res.error) return alert(res.error);
  state = res.game;
  renderBoard(state);
  showInfo(state);
}
document.getElementById('refresh').addEventListener('click', refresh);
function showInfo(game) {
  let html = `Game: ${game.id} | Turn: ${game.turn}`;
  if (game.winner) html += ` | Winner: ${game.winner}`;
  html += `<br>Players: A=${game.players.A ? game.players.A.username : '—'} B=${game.players.B ? game.players.B.username : '—'}`;
  infoEl.innerHTML = html;
}
function dirToDelta(dir) {
  switch (dir) {
    case 'up': return { r: -1, c: 0 };
    case 'down': return { r: 1, c: 0 };
    case 'left': return { r: 0, c: -1 };
    case 'right': return { r: 0, c: 1 };
  }
}

document.querySelectorAll('.move-controls button').forEach(btn => {
  btn.addEventListener('click', async () => {
    if (!currentGameId || !myPlayerKey) return alert('join or start a game first');
    if (!state) await refresh();
    if (state.winner) return alert('game finished');
    if (state.turn !== myPlayerKey) return alert("not your turn");
    const delta = dirToDelta(btn.dataset.dir);
    const me = state.players[myPlayerKey];
    const to = { r: me.pos.r + delta.r, c: me.pos.c + delta.c };
    const res = await api('/move', 'POST', { gameId: currentGameId, playerKey: myPlayerKey, to });
    if (res.error) return alert(res.error);
    state = res.game;
    renderBoard(state);
    showInfo(state);
  });
});
setInterval(() => {
  if (currentGameId) refresh();
}, 3000);
