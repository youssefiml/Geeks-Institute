import fs from 'fs/promises';
import path from 'path';
import bcrypt from 'bcrypt';
import config from '../config/user_config.js';

class UserModel {
  constructor() {
    this.filePath = config.usersFilePath;
    this.ensureDataDirectory();
  }

  // Ensure data directory exists
  async ensureDataDirectory() {
    const dataDir = path.dirname(this.filePath);
    try {
      await fs.access(dataDir);
    } catch {
      await fs.mkdir(dataDir, { recursive: true });
    }
  }

  // Read all users from file
  async getAllUsers() {
    try {
      const data = await fs.readFile(this.filePath, 'utf8');
      return JSON.parse(data);
    } catch (error) {
      if (error.code === 'ENOENT') {
        await this.saveUsers([]);
        return [];
      }
      throw error;
    }
  }

  // Find user by ID
  async findUserById(id) {
    const users = await this.getAllUsers();
    return users.find(user => user.id === id);
  }

  // Find user by username
  async findUserByUsername(username) {
    const users = await this.getAllUsers();
    return users.find(user => user.username.toLowerCase() === username.toLowerCase());
  }

  // Save users to file
  async saveUsers(users) {
    await fs.writeFile(this.filePath, JSON.stringify(users, null, 2), 'utf8');
  }

  // Register new user
  async registerUser(userData) {
    const users = await this.getAllUsers();
    
    // Check if username already exists
    const existingUser = await this.findUserByUsername(userData.username);
    if (existingUser) {
      throw new Error(config.messages.userExists);
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(userData.password, config.saltRounds);

    const newUser = {
      id: this.generateId(),
      username: userData.username,
      email: userData.email,
      password: hashedPassword,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    users.push(newUser);
    await this.saveUsers(users);
    
    // Return user without password
    const { password, ...userWithoutPassword } = newUser;
    return userWithoutPassword;
  }

  // Verify user login
  async verifyLogin(username, password) {
    const user = await this.findUserByUsername(username);
    
    if (!user) {
      return null;
    }

    const isPasswordValid = await bcrypt.compare(password, user.password);
    
    if (!isPasswordValid) {
      return null;
    }

    // Return user without password
    const { password: _, ...userWithoutPassword } = user;
    return userWithoutPassword;
  }

  // Update user by ID
  async updateUser(id, updateData) {
    const users = await this.getAllUsers();
    const userIndex = users.findIndex(user => user.id === id);

    if (userIndex === -1) {
      return null;
    }

    // If password is being updated, hash it
    if (updateData.password) {
      updateData.password = await bcrypt.hash(updateData.password, config.saltRounds);
    }

    users[userIndex] = {
      ...users[userIndex],
      ...updateData,
      id: users[userIndex].id,
      createdAt: users[userIndex].createdAt,
      updatedAt: new Date().toISOString()
    };

    await this.saveUsers(users);
    
    // Return user without password
    const { password, ...userWithoutPassword } = users[userIndex];
    return userWithoutPassword;
  }

  // Delete user by ID
  async deleteUser(id) {
    const users = await this.getAllUsers();
    const userIndex = users.findIndex(user => user.id === id);

    if (userIndex === -1) {
      return null;
    }

    const deletedUser = users.splice(userIndex, 1)[0];
    await this.saveUsers(users);
    
    // Return user without password
    const { password, ...userWithoutPassword } = deletedUser;
    return userWithoutPassword;
  }

  // Generate unique ID
  generateId() {
    return Date.now().toString() + Math.random().toString(36).substr(2, 9);
  }

  // Get users count
  async getUsersCount() {
    const users = await this.getAllUsers();
    return users.length;
  }

  // Get all users without passwords (for listing)
  async getAllUsersWithoutPasswords() {
    const users = await this.getAllUsers();
    return users.map(({ password, ...user }) => user);
  }
}

module.exports = new UserModel();
