import bcrypt from 'bcrypt';
const User = require('../models/user.js');
const HashPwd = require('../models/hashpwd.js');
const db = require('../config/database');
const getUsers = async (req, res) => {
  try {
    const users = await User.findAll();
    res.json(users);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to fetch users' });
  }
};
const getUser = async (req, res) => {
  try {
    const id = req.params.id;
    const user = await User.findById(id);
    if (!user) return res.status(404).json({ message: 'User not found' });
    res.json(user);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to fetch user' });
  }
};
const registerUser = async (req, res) => {
  const { email, username, password, first_name, last_name } = req.body;

  try {
    await db.transaction(async trx => {
      const user = await User.create({ email, username, first_name, last_name }, trx);
      const hashed = await bcrypt.hash(password, 10);
      await HashPwd.create({ username, password: hashed }, trx);
    });
    res.json({ message: 'User registered successfully' });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Registration failed' });
  }
};
const loginUser = async (req, res) => {
  try {
    const { username, password } = req.body;
    const user = await HashPwd.findByUsername(username);
    if (!user) return res.status(404).json({ error: 'User not found' });

    const match = await bcrypt.compare(password, user.password);
    if (!match) return res.status(401).json({ error: 'Invalid password' });

    res.json({ message: 'Login successful' });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Login failed' });
  }
};
const updateUser = async (req, res) => {
  const id = req.params.id;
  const { email, username, first_name, last_name, password } = req.body;

  try {
    await db.transaction(async trx => {
      await User.update(id, { email, username, first_name, last_name }, trx);

      if (password) {
        const hashed = await bcrypt.hash(password, 10);
        await HashPwd.updatePassword(id, hashed, trx); // updatePassword doit accepter trx
      }
    });
    res.json({ message: 'User updated successfully' });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Update failed' });
  }
};
module.exports = { getUsers, getUser, registerUser, loginUser, updateUser };