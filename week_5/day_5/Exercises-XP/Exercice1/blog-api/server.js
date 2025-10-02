const express = require('express');

const app = express();
const PORT = 3000;

app.use(express.json());

const blogPosts = [
  {
    id: 1,
    title: "Getting Started with Node.js",
    content: "Node.js is a runtime environment that allows you to run JavaScript on the server."
  },
  {
    id: 2,
    title: "Understanding Express.js",
    content: "Express.js is a minimal and flexible Node.js web application framework."
  },
  {
    id: 3,
    title: "Intro to MongoDB",
    content: "MongoDB is a NoSQL database that stores data in JSON-like documents."
  }
];

app.get('/posts', (req, res) => {
  res.json(blogPosts);
});

app.get('/posts/:id', (req, res) => {
    const postId = parseInt(req.params.id, 10);
    const post = blogPosts.find(b => b.id === postId);

    if (post) {
        res.json(post);
    } else {
        res.status(404).json({ message: "Post not found" });
    }
});

app.post('/posts', (req, res) => {
    const newPost = {
        id: blogPosts.length + 1,
        title: req.body.title || "Untitled Post",
        content: req.body.content || "No content"
    };
    try {
        blogPosts.push(newPost);
        res.status(201).json(newPost);
    } catch (error) {
        res.status(500).json({ message: "Error creating post" });
    }
});

app.put('/posts/:id', (req, res) => {
    const postId = parseInt(req.params.id, 10);
    const post = blogPosts.find(b => b.id === postId);

    if (post) {
        post.title = req.body.title || post.title;
        post.content = req.body.content || post.content;
        res.json(post);
    } else {
        res.status(404).json({ message: "Post not found" });
    }   
});

app.delete('/posts/:id', (req, res) => {
    const postId = parseInt(req.params.id, 10);
    const post = blogPosts.find(b => b.id === postId);
    if (post) {
        const index = blogPosts.indexOf(post);
        blogPosts.splice(index, 1);
        res.json({ message: "Post deleted successfully" });
    } else {  
        res.status(404).json({ message: "Post not found" });
    }
});


app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
  console.log('Available endpoints:');
  console.log(`GET          http://localhost:${PORT}/posts`);
  console.log(`GET by Id    http://localhost:${PORT}/posts/:id`);
  console.log(`POST         http://localhost:${PORT}/posts`);
  console.log(`PUT by Id    http://localhost:${PORT}/posts/:id`)
});