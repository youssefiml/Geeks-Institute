import express from "express";
import http from "http";
import path from "path";
import { Server } from "socket.io";

const app = express();
const server = http.createServer(app);
const io = new Server(server);

app.use(express.static(path.join(__dirname, "public")));
const PORT = process.env.PORT || 3000;
const rooms = {};
const HISTORY_LIMIT = 50;

function ensureRoom(room) {
  if (!rooms[room]) rooms[room] = { users: {}, history: [] };
}

io.on("connection", (socket) => {
  console.log("Socket connected:", socket.id);

  socket.on("joinRoom", ({ username, room }) => {
    if (!username || !room) return;

    socket.join(room);
    ensureRoom(room);

    rooms[room].users[socket.id] = { username };
    socket.emit("roomHistory", rooms[room].history);

    const joinMsg = {
      system: true,
      text: `${username} a rejoint la salle.`,
      ts: Date.now(),
    };

    rooms[room].history.push(joinMsg);
    if (rooms[room].history.length > HISTORY_LIMIT) rooms[room].history.shift();

    io.to(room).emit("message", joinMsg);
    io.to(room).emit("roomUsers", {
      users: Object.values(rooms[room].users).map((u) => u.username),
    });

    console.log(`${username} joined ${room}`);
  });

  socket.on("chatMessage", ({ room, text }) => {
    if (!room || !text) return;
    ensureRoom(room);

    const user = rooms[room].users[socket.id];
    const payload = {
      username: user ? user.username : "Unknown",
      text,
      ts: Date.now(),
    };

    rooms[room].history.push(payload);
    if (rooms[room].history.length > HISTORY_LIMIT) rooms[room].history.shift();

    io.to(room).emit("message", payload);
  });

  socket.on("updateProfile", ({ room, username }) => {
    if (room && rooms[room] && rooms[room].users[socket.id]) {
      rooms[room].users[socket.id].username = username;
      io.to(room).emit("roomUsers", {
        users: Object.values(rooms[room].users).map((u) => u.username),
      });
    }
  });

  socket.on("typing", ({ room, typing }) => {
    socket.to(room).emit("typing", {
      username: rooms[room]?.users[socket.id]?.username || "Someone",
      typing,
    });
  });

  socket.on("disconnect", () => {
    for (const roomName of Object.keys(rooms)) {
      const room = rooms[roomName];

      if (room.users[socket.id]) {
        const username = room.users[socket.id].username;
        delete room.users[socket.id];

        const leaveMsg = {
          system: true,
          text: `${username} a quitté la salle.`,
          ts: Date.now(),
        };

        room.history.push(leaveMsg);
        if (room.history.length > HISTORY_LIMIT) room.history.shift();

        io.to(roomName).emit("message", leaveMsg);
        io.to(roomName).emit("roomUsers", {
          users: Object.values(room.users).map((u) => u.username),
        });

        console.log(`${username} disconnected from ${roomName}`);
      }

      if (Object.keys(room.users).length === 0 && room.history.length === 0) {
        delete rooms[roomName];
      }
    }
  });
});

server.listen(PORT, () => {
  console.log(`Server listening on http://localhost:${PORT}`);
});