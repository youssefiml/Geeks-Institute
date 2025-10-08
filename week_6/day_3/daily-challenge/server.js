import express from 'express';
import userRoutes from './routes/userRoutes.js';
import { sequelize } from './config/db.js';


const app = express();

app.use(express.json());
app.use('/api', userRoutes);

const PORT = 5000;

sequelize.sync({ alter: true }).then(() => {
    app.listen(PORT, () => {
        console.log(`Server running at http://localhost:${PORT}`)
    });
});