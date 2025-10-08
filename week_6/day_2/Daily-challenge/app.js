import express from "express";
import quizRouter from "./routes/quiz.routes.js";

const app = express();

app.use(express.urlencoded({ extended: true }));

app.use("/quiz", quizRouter);

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`🎯 Trivia Quiz running at http://localhost:${PORT}/quiz`);
});