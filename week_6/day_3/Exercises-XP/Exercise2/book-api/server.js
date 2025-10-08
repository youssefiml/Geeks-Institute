import express from 'express';
import bodyParser from 'body-parser';
import cors from 'cors';
import { connectDB } from './config/database.js';
import bookRouter from './routes/books.route.js';

const app = express();
const PORT = 3000;

app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.json());
app.use(cors());

connectDB();

app.use('/books', bookRouter);

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${port}`)
});