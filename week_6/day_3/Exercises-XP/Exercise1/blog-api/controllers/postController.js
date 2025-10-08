import Post from '../models/postModel.js';

const postController = {
  async getAll(req, res, next) {
    try {
      const posts = await Post.getAll();
      res.json(posts);
    } catch (err) {
      next(err);
    }
  },

  async getById(req, res, next) {
    try {
      const post = await Post.getById(req.params.id);
      if (!post) return res.status(404).json({ message: 'Post not found' });
      res.json(post);
    } catch (err) {
      next(err);
    }
  },

  async create(req, res, next) {
    try {
      const { title, content } = req.body;
      const newPost = await Post.create(title, content);
      res.status(201).json(newPost);
    } catch (err) {
      next(err);
    }
  },

  async update(req, res, next) {
    try {
      const { title, content } = req.body;
      const updatedPost = await Post.update(req.params.id, title, content);
      if (!updatedPost) return res.status(404).json({ message: 'Post not found' });
      res.json(updatedPost);
    } catch (err) {
      next(err);
    }
  },

  async delete(req, res, next) {
    try {
      const result = await Post.delete(req.params.id);
      res.json(result);
    } catch (err) {
      next(err);
    }
  },
};

export default postController;