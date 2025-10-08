import express from 'express';
import postController from './controllers/postController.js';

const app = express();
const PORT = 3000;
app.use(express.json());

const router = express.Router();

router.get('/', postController.getAll);
router.get('/:id', postController.getById);
router.post('/', postController.create);
router.put('/:id', postController.update);
router.delete('/:id', postController.delete);

app.listen(PORT, () => {
    console.log('Server is running on http://localhost:3000');
});