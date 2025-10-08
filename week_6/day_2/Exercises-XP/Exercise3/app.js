import express from "express";
import routes from './routes/books.routes.js';

const app = express();
const PORT = 9090;

app.use(express.json());

app.use('/books', routes);

app.listen(PORT, () => {
    console.log(`server is runing on http://localhost:${PORT}`)
});