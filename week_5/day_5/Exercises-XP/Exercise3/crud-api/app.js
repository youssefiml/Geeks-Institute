import express from 'express';
import { fetchPosts } from './data/dataService.js';

const app = express();
const PORT = 5000;



app.get('/posts', async (req, res) => {
    try {
        const response = await fetchPosts();
        res.json(response.data);
        console.log(data);
        console.log("the data has been successfully retrieved and sent to the client.");
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch posts' });
    }
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}/posts`);
});