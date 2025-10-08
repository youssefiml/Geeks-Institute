import express from "express";
const router = express.Router();

const triviaQuestions = [
  { question: "What is the capital of France?", answer: "Paris" },
  { question: "Which planet is known as the Red Planet?", answer: "Mars" },
  { question: "What is the largest mammal in the world?", answer: "Blue whale" },
  { question: "What is the smallest country in the world?", answer: "Vatican City" },
  { question: "What is the chemical symbol for gold?", answer: "Au" },
  { question: "What is the largest ocean in the world?", answer: "Pacific Ocean" },
  { question: "What is the highest mountain in the world?", answer: "Mount Everest" },
  { question: "What is the smallest planet in the solar system?", answer: "Mercury" },
  { question: "What is the largest planet in the solar system?", answer: "Jupiter" },
  { question: "Who is the best Messi or Ronaldo?", answer: "Messi" }
];

let currentQuestionIndex = 0;
let score = 0;

const generatePage = (content) => `
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Trivia Quiz</title>
<style>
  body {
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #89f7fe, #66a6ff);
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
  }
  .quiz-container {
    background: white;
    padding: 30px 40px;
    border-radius: 15px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    width: 100%;
    max-width: 500px;
    text-align: center;
  }
  h1 {
    margin-bottom: 20px;
    color: #333;
  }
  p {
    font-size: 1.1em;
  }
  input[type="text"] {
    width: 80%;
    padding: 10px;
    margin: 15px 0;
    border-radius: 8px;
    border: 1px solid #ccc;
    font-size: 1em;
  }
  button {
    padding: 10px 20px;
    font-size: 1em;
    border-radius: 8px;
    border: none;
    background-color: #66a6ff;
    color: white;
    cursor: pointer;
    transition: 0.3s;
  }
  button:hover {
    background-color: #5588e0;
  }
  .feedback {
    font-size: 1.2em;
    margin: 10px 0;
  }
  .correct { color: green; }
  .wrong { color: red; }
  a { 
    display: inline-block; 
    margin-top: 15px; 
    text-decoration: none; 
    color: #66a6ff; 
    font-weight: bold;
  }
</style>
</head>
<body>
  <div class="quiz-container">
    ${content}
  </div>
</body>
</html>
`;

router.get("/", (req, res) => {
  if (currentQuestionIndex >= triviaQuestions.length) {
    return res.redirect("/quiz/score");
  }
  const currentQ = triviaQuestions[currentQuestionIndex];
  const content = `
    <h1>Trivia Quiz</h1>
    <p>Question ${currentQuestionIndex + 1}: ${currentQ.question}</p>
    <form method="POST">
      <input type="text" name="answer" placeholder="Your answer" required />
      <br/>
      <button type="submit">Submit</button>
    </form>
  `;
  res.send(generatePage(content));
});

router.post("/", (req, res) => {
  const userAnswer = req.body.answer?.trim();
  const currentQ = triviaQuestions[currentQuestionIndex];
  let feedback;
  
  if (userAnswer.toLowerCase() === currentQ.answer.toLowerCase()) {
    score++;
    feedback = `<p class="feedback correct">✅ Correct!</p>`;
  } else {
    feedback = `<p class="feedback wrong">❌ Wrong! Correct answer: ${currentQ.answer}</p>`;
  }

  currentQuestionIndex++;

  if (currentQuestionIndex >= triviaQuestions.length) {
    return res.redirect("/quiz/score");
  }

  const nextQ = triviaQuestions[currentQuestionIndex];
  const content = `
    ${feedback}
    <p>Next Question: ${nextQ.question}</p>
    <form method="POST">
      <input type="text" name="answer" placeholder="Your answer" required />
      <br/>
      <button type="submit">Submit</button>
    </form>
  `;

  res.send(generatePage(content));
});

router.get("/score", (req, res) => {
  const content = `
    <h1>🎉 Quiz Finished!</h1>
    <p>Your final score: ${score}/${triviaQuestions.length}</p>
    <a href="/quiz/reset">Play Again</a>
  `;
  res.send(generatePage(content));
});

router.get("/reset", (req, res) => {
  currentQuestionIndex = 0;
  score = 0;
  res.redirect("/quiz");
});

export default router;