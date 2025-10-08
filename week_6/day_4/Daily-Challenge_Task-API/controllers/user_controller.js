import userModel from '../models/user_model.js';
import config from '../config/user_config.js';

class UserController {
  async register(req, res) {
    try {
      const { username, email, password } = req.body;

      const validationError = this.validateRegistration({ username, email, password });
      if (validationError) {
        return res.status(400).json({
          success: false,
          error: validationError
        });
      }

      const userData = {
        username: username.trim(),
        email: email.trim(),
        password
      };

      const newUser = await userModel.registerUser(userData);

      res.status(201).json({
        success: true,
        message: config.messages.userCreated,
        data: newUser
      });
    } catch (error) {
      console.error('Error in register:', error);
      
      if (error.message === config.messages.userExists) {
        return res.status(409).json({
          success: false,
          error: error.message
        });
      }

      res.status(500).json({
        success: false,
        error: config.messages.serverError
      });
    }
  }

  async login(req, res) {
    try {
      const { username, password } = req.body;

      if (!username || !password) {
        return res.status(400).json({
          success: false,
          error: 'Username and password are required'
        });
      }

      const user = await userModel.verifyLogin(username, password);

      if (!user) {
        return res.status(401).json({
          success: false,
          error: config.messages.loginFailed
        });
      }

      res.status(200).json({
        success: true,
        message: config.messages.loginSuccess,
        data: user
      });
    } catch (error) {
      console.error('Error in login:', error);
      res.status(500).json({
        success: false,
        error: config.messages.serverError
      });
    }
  }

  async getAllUsers(req, res) {
    try {
      const users = await userModel.getAllUsersWithoutPasswords();
      
      res.status(200).json({
        success: true,
        count: users.length,
        data: users
      });
    } catch (error) {
      console.error('Error in getAllUsers:', error);
      res.status(500).json({
        success: false,
        error: config.messages.serverError
      });
    }
  }

  async getUserById(req, res) {
    try {
      const { id } = req.params;
      const user = await userModel.findUserById(id);

      if (!user) {
        return res.status(404).json({
          success: false,
          error: config.messages.userNotFound
        });
      }

      const { password, ...userWithoutPassword } = user;

      res.status(200).json({
        success: true,
        data: userWithoutPassword
      });
    } catch (error) {
      console.error('Error in getUserById:', error);
      res.status(500).json({
        success: false,
        error: config.messages.serverError
      });
    }
  }

  async updateUser(req, res) {
    try {
      const { id } = req.params;
      const { username, email, password } = req.body;

      const validationError = this.validateUpdate({ username, email, password });
      if (validationError) {
        return res.status(400).json({
          success: false,
          error: validationError
        });
      }

      const updateData = {};
      if (username) updateData.username = username.trim();
      if (email) updateData.email = email.trim();
      if (password) updateData.password = password;

      const updatedUser = await userModel.updateUser(id, updateData);

      if (!updatedUser) {
        return res.status(404).json({
          success: false,
          error: config.messages.userNotFound
        });
      }

      res.status(200).json({
        success: true,
        message: config.messages.userUpdated,
        data: updatedUser
      });
    } catch (error) {
      console.error('Error in updateUser:', error);
      res.status(500).json({
        success: false,
        error: config.messages.serverError
      });
    }
  }

  async deleteUser(req, res) {
    try {
      const { id } = req.params;
      const deletedUser = await userModel.deleteUser(id);

      if (!deletedUser) {
        return res.status(404).json({
          success: false,
          error: config.messages.userNotFound
        });
      }

      res.status(200).json({
        success: true,
        message: config.messages.userDeleted,
        data: deletedUser
      });
    } catch (error) {
      console.error('Error in deleteUser:', error);
      res.status(500).json({
        success: false,
        error: config.messages.serverError
      });
    }
  }

  validateRegistration(data) {
    const { username, email, password } = data;
    const { minUsernameLength, maxUsernameLength, minPasswordLength, maxPasswordLength } = config.validation;

    if (!username || typeof username !== 'string' || username.trim() === '') {
      return 'Username is required';
    }

    if (username.length < minUsernameLength) {
      return `Username must be at least ${minUsernameLength} characters`;
    }

    if (username.length > maxUsernameLength) {
      return `Username must not exceed ${maxUsernameLength} characters`;
    }

    if (!email || typeof email !== 'string' || !this.isValidEmail(email)) {
      return 'Valid email is required';
    }

    if (!password || typeof password !== 'string') {
      return 'Password is required';
    }

    if (password.length < minPasswordLength) {
      return `Password must be at least ${minPasswordLength} characters`;
    }

    if (password.length > maxPasswordLength) {
      return `Password must not exceed ${maxPasswordLength} characters`;
    }

    return null;
  }

  validateUpdate(data) {
    const { username, email, password } = data;
    const { minUsernameLength, maxUsernameLength, minPasswordLength, maxPasswordLength } = config.validation;

    if (username !== undefined) {
      if (typeof username !== 'string' || username.trim() === '') {
        return 'Username must be a non-empty string';
      }

      if (username.length < minUsernameLength) {
        return `Username must be at least ${minUsernameLength} characters`;
      }

      if (username.length > maxUsernameLength) {
        return `Username must not exceed ${maxUsernameLength} characters`;
      }
    }

    if (email !== undefined) {
      if (typeof email !== 'string' || !this.isValidEmail(email)) {
        return 'Valid email is required';
      }
    }

    if (password !== undefined) {
      if (typeof password !== 'string') {
        return 'Password must be a string';
      }

      if (password.length < minPasswordLength) {
        return `Password must be at least ${minPasswordLength} characters`;
      }

      if (password.length > maxPasswordLength) {
        return `Password must not exceed ${maxPasswordLength} characters`;
      }
    }

    return null;
  }

  isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }
}

export default new UserController();