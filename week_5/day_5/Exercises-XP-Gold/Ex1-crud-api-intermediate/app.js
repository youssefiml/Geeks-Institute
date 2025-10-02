// Part 1
import express from 'express';
import axios from 'axios';


const app = express();
const PORT = 5000;
const BASE_URL = 'https://jsonplaceholder.typicode.com/posts';

app.use(express.json());

// Part 2

app.get('/api/posts', async (req, res) => {
  try {
    const response = await axios.get(BASE_URL);
    res.json(response.data);
  } catch (error) {
    res.status(404).json({ message: 'Error fetching posts', error: error.message });
  }
});

app.get('/api/posts/:id', async (req, res) => {
  try {
    const response = await axios.get(`${BASE_URL}/${req.params.id}`);
    res.json(response.data);
  } catch (error) {
    res.status(404).json({ message: 'Error fetching post', error: error.message });
  }
});

app.post('/api/posts', async (req, res) => {
  try {
    const response = await axios.post(BASE_URL, req.body);
    res.status(201).json(response.data);
  } catch (error) {
    res.status(404).json({ message: 'Error creating post', error: error.message });
  }
});

app.put('/api/posts/:id', async (req, res) => {
  try {
    const response = await axios.put(`${BASE_URL}/${req.params.id}`, req.body);
    res.json(response.data);
  } catch (error) {
    res.status(404).json({ message: 'Error updating post', error: error.message });
  }
});

app.delete('/api/posts/:id', async (req, res) => {
  try {
    await axios.delete(`${BASE_URL}/${req.params.id}`);
    res.json({ message: 'Post deleted successfully' });
  } catch (error) {
    res.status(404).json({ message: 'Error deleting post', error: error.message });
  }
});

app.listen(PORT, () => {
    console.log(`server is runing on http://localhost:${PORT}/api/posts`)
});