import express from 'express';
import path from 'path';
import config from './config/user_config.js';
import userRoutes from './routes/user_routes.js';

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use(express.static(path.join(__dirname, 'public')));

if (config.env === 'development') {
  app.use((req, res, next) => {
    console.log(`${req.method} ${req.path}`);
    next();
  });
}

app.get('/', (req, res) => {
  res.json({
    message: 'User Management API',
    version: '1.0.0',
    pages: {
      'GET /register.html': 'Registration page',
      'GET /login.html': 'Login page'
    },
    endpoints: {
      'POST /api/register': 'Register new user',
      'POST /api/login': 'Login user',
      'GET /api/users': 'Get all users',
      'GET /api/users/:id': 'Get user by ID',
      'PUT /api/users/:id': 'Update user by ID',
      'DELETE /api/users/:id': 'Delete user by ID'
    }
  });
});

app.use('/api', userRoutes);

app.use((req, res) => {
  res.status(404).json({
    success: false,
    error: 'Route not found'
  });
});

app.use((err, req, res, next) => {
  console.error('Unhandled error:', err);
  res.status(500).json({
    success: false,
    error: config.messages.serverError
  });
});

app.listen(config.port, () => {
  console.log(`Server running on http://localhost:${config.port}`);
});

export default app;