import express from "express";
import about from './routes/About.routes.js';
import home from './routes/Home.routes.js'

const app = express();
const PORT = 3030;

app.use(express.json());

app.use('/', home);
app.use('/About', about);

app.listen(PORT, () => {
    console.log(`server is runing on http://localhost:${PORT}`)
});