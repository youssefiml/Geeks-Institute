import pool from '../config/db.js';

const Post = {
  async getAll() {
    const result = await pool.query('SELECT * FROM posts ORDER BY id ASC');
    return result.rows;
  },

  async getById(id) {
    const result = await pool.query('SELECT * FROM posts WHERE id = $1', [id]);
    return result.rows[0];
  },

  async create(title, content) {
    const result = await pool.query(
      'INSERT INTO posts (title, content) VALUES ($1, $2) RETURNING *',
      [title, content]
    );
    return result.rows[0];
  },

  async update(id, title, content) {
    const result = await pool.query(
      'UPDATE posts SET title = $1, content = $2 WHERE id = $3 RETURNING *',
      [title, content, id]
    );
    return result.rows[0];
  },

  async delete(id) {
    await pool.query('DELETE FROM posts WHERE id = $1', [id]);
    return { message: 'Post deleted successfully' };
  },
};

export default Post;