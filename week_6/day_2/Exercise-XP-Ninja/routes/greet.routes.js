import express from "express";

const router = express.Router();

const emojis = ["😀", "🎉", "🌟", "🎈", "👋"];

router.get("/", (req, res) => {
  const emojiOptions = emojis
    .map(e => `<option value="${e}">${e}</option>`)
    .join("");

  res.send(`
    <html>
      <head>
        <title>Emoji Greeting</title>
        <link rel="stylesheet" href="/style.css">
      </head>
      <body>
        <div class="container">
          <h1>👋</h1>
          <form action="/greet" method="POST">
            <label for="name">Your Name:</label>
            <input type="text" name="name" id="name" required>

            <label for="emoji">Choose an Emoji:</label>
            <select name="emoji" id="emoji" required>
              ${emojiOptions}
            </select>

            <button type="submit">Greet Me</button>
          </form>
        </div>
      </body>
    </html>
  `);
});

router.post("/greet", (req, res) => {
  const { name, emoji } = req.body;

  if (!name || name.trim() === "") {
    return res.send(`
      <html>
        <body style="text-align:center; font-family:sans-serif;">
          <h2>Please enter your name!</h2>
          <a href="/">⬅ Go back</a>
        </body>
      </html>
    `);
  }

  res.send(`
    <html>
      <head>
        <title>Greeting</title>
        <link rel="stylesheet" href="/style.css">
      </head>
      <body>
        <div class="greeting">
          <h1>${emoji} Hello, ${name}! ${emoji}</h1>
          <a href="/">⬅ Greet someone else</a>
        </div>
      </body>
    </html>
  `);
});

export default router;