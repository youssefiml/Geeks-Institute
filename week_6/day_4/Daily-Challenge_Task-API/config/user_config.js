import path from 'path';

const config = {
  port: process.env.PORT || 3000,
  env: process.env.NODE_ENV || 'development',
  
  usersFilePath: path.join(__dirname, '..', 'data', 'users.json'),
  
  saltRounds: 10,
  
  validation: {
    minUsernameLength: 3,
    maxUsernameLength: 30,
    minPasswordLength: 6,
    maxPasswordLength: 100
  },
  
  messages: {
    userCreated: 'User registered successfully',
    userUpdated: 'User updated successfully',
    userDeleted: 'User deleted successfully',
    userNotFound: 'User not found',
    loginSuccess: 'Login successful',
    loginFailed: 'Invalid username or password',
    validationError: 'Validation error',
    serverError: 'Internal server error',
    userExists: 'Username already exists'
  }
};

export default config;