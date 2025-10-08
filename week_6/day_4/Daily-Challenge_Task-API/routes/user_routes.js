import express from 'express';
import userController from '../controllers/user_controller.js';

const router = express.Router();

router.post('/register', userController.register.bind(userController));
router.post('/login', userController.login.bind(userController));

router.get('/users', userController.getAllUsers.bind(userController));
router.get('/users/:id', userController.getUserById.bind(userController));
router.put('/users/:id', userController.updateUser.bind(userController));
router.delete('/users/:id', userController.deleteUser.bind(userController));

export default router;