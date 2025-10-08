import express from 'express';
import postsRouter from './routes/posts.routes.js';

const app = express();
const PORT = 3000;

app.use(express.json());

app.use('/posts', postsRouter);

app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});