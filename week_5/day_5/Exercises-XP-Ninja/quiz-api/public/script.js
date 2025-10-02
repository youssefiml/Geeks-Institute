let questions = [];
let currentQuestion = 0;
let score = 0;

async function loadQuestions() {
  try {
    const res = await fetch('/api/questions');
    questions = await res.json();
    currentQuestion = 0;
    score = 0;
    document.getElementById('score').textContent = `Score: ${score}`;
    showQuestion(currentQuestion);
  } catch (err) {
    console.error(err);
  }
}

function showQuestion(index) {
  const q = questions[index];
  if (!q) return;

  document.getElementById('question-text').textContent = q.question;
  const answersDiv = document.getElementById('answers');
  answersDiv.innerHTML = '';

  q.answers.forEach(answer => {
    const btn = document.createElement('button');
    btn.textContent = answer;
    btn.addEventListener('click', async () => {
      await checkAnswer(q.id, answer);
      Array.from(answersDiv.children).forEach(b => b.disabled = true);
    });
    answersDiv.appendChild(btn);
  });
}

async function checkAnswer(id, answer) {
  try {
    const res = await fetch('/api/answers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id, answer })
    });
    const data = await res.json();
    const buttons = document.querySelectorAll('#answers button');

    buttons.forEach(btn => {
      if (btn.textContent === questions.find(q => q.id === id).correct) {
        btn.style.backgroundColor = 'green';
      } else if (btn.textContent === answer) {
        btn.style.backgroundColor = 'red';
      }
      btn.disabled = true;
    });

    if (data.correct) score++;
    document.getElementById('score').textContent = `Score: ${score}`;
  } catch (err) {
    console.error(err);
  }
}

document.getElementById('next-btn').addEventListener('click', () => {
  currentQuestion++;
  if (currentQuestion < questions.length) {
    showQuestion(currentQuestion);
  } else {
    document.getElementById('question-text').textContent =
      `Quiz finished! Your score: ${score}/${questions.length}`;
    document.getElementById('answers').innerHTML = '';
    const nextBtn = document.getElementById('next-btn');
    nextBtn.textContent = "Restart Quiz";
    nextBtn.onclick = () => {
      loadQuestions();
    };
  }
});

loadQuestions();