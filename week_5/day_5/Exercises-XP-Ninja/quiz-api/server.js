import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

const quizQuestions = [
  {
      id: 1,
      question: "Which language runs in a server?",
      answers: ["Python", "PHP", "JavaScript", "Java", "All of the above"],
      correct: "All of the above"
  },
  {
    id: 2,
    question: "Which language runs in a browser?",
    answers: ["Python", "C++", "JavaScript", "Java"],
    correct: "JavaScript"
  },
  {
    id: 3,
    question: "What does HTML stand for?",
    answers: ["Hyper Text Markup Language", "Home Tool Markup Language", "Hyperlinks and Text Markup Language", "Hyper Text Multiple Language"],
    correct: "Hyper Text Markup Language"
  },
  {
    id: 4,
    question: "What does CSS stand for?",
    answers: ["Colorful Style Sheets", "Computer Style Sheets", "Cascading Style Sheets", "Creative Style Sheets"],
    correct: "Cascading Style Sheets"
  },
  {
    id: 5,
    question: "What does SQL stand for?",
    answers: ["Structured Query Language", "Stylish Question Language", "Stylesheet Query Language", "Superior Question Language"],
    correct: "Structured Query Language"
  },
  {
    id: 6,
    question: "What does HTTP stand for?",
    answers: ["Hypertext Transfer Protocol", "Hypertext Test Protocol", "Hypertext Transfer Program", "Hypertext Test Program"],
    correct: "Hypertext Transfer Protocol"
  },
  {
    id: 7,
    question: "What does URL stand for?",
    answers: ["Uniform Resource Locator", "Uniform Resource Link", "Uniform Resource Language", "Uniform Resource Location"],
    correct: "Uniform Resource Locator"
  },
  {
    id: 8,
    question: "What does XML stand for?",
    answers: ["eXtensible Markup Language", "eXtensible Markup Line", "eXtensible Markup List", "eXtensible Markup Loop"],
    correct: "eXtensible Markup Language"
  },
  {
    id: 9,
    question: "What does JSON stand for?",
    answers: ["Java Object Notation", "JavaScript Object Notation", "JavaScript Open Notation", "Java Open Notation"],
    correct: "JavaScript Object Notation"
  },
  {
    id: 10,
    question: "What does API stand for?",
    answers: ["Application Programming Interface", "Application Program Interface", "Application Programming Information", "Application Program Information"],
    correct: "Application Programming Interface"
  }
];

app.get('/api/questions', (req, res) => {
  res.json(quizQuestions);
});

app.get('/api/questions/:id', (req, res) => {
  const questionId = parseInt(req.params.id, 10);
  const question = quizQuestions.find(q => q.id === questionId);
  if (question) {
    res.json(question);
  } else {
    res.status(404).json({ message: 'Question not found' });
  }
});

app.get('/api/questions/random', (req, res) => {
  const shuffled = [...quizQuestions].sort(() => 0.5 - Math.random());
  res.json(shuffled.slice(0, 5));
});

app.post('/api/answers', (req, res) => {
    const { id, answer } = req.body;

    const question = quizQuestions.find(q => q.id === id);
    if (!question) {
        return res.status(404).json({ message: "Question not found" });
    }

    const isCorrect = question.correct === answer;
    res.json({ correct: isCorrect });
});

app.put('/api/questions/:id', (req, res) => {
  const questionId = parseInt(req.params.id, 10);
  const question = quizQuestions.find(q => q.id === questionId);
  if (question) {
    question.question = req.body.question;
    question.answers = req.body.answers;
    question.correct = req.body.correct;
    res.json(question);
  } else {
    res.status(404).json({ message: 'Question not found' });
  }
});

app.delete('/api/questions/:id', (req, res) => {
  const questionId = parseInt(req.params.id, 10);
  const questionIndex = quizQuestions.findIndex(q => q.id === questionId);
  if (questionIndex !== -1) {
    quizQuestions.splice(questionIndex, 1);
    res.json({ message: 'Question deleted successfully' });
  } else {
    res.status(404).json({ message: 'Question not found' });
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}/api/questions`);
});