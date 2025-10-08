import express from "express";
import routes from './routes/todos.routes.js';

const app = express();
const PORT = 4040;

app.use(express.json());

app.use('/todos', routes);

app.listen(PORT, () => {
    console.log(`server is runing on http://localhost:${PORT}`)
});