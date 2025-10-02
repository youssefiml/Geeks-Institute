import express from 'express';

const app = express();
const PORT = 5000;

app.use(express.json());

const books = [
  {
    id: 1,
    title: "Clean Code",
    author: "Robert C. Martin",
    publishedYear: 2008
  },
  {
    id: 2,
    title: "The Pragmatic Programmer",
    author: "Andrew Hunt & David Thomas",
    publishedYear: 1999
  },
  {
    id: 3,
    title: "You Don't Know JS",
    author: "Kyle Simpson",
    publishedYear: 2014
  }
];

app.get('/api/books', (req, res) => {
  res.json(books);
});

app.get('/api/books/:id', (req, res) => {
    const bookId = parseInt(req.params.id, 10);
    const book = books.find(b => b.id === bookId);
    if (book) {
      res.json(book);
      res.status(200);
    } else {
      res.status(404).json({ message: 'Book not found' });
    }
});

app.post('/api/books', (req, res) => {
    const newBook = {
            id: books.length + 1,
            title: req.body.title || "Untitled Post",
            author: req.body.author || "No author",
            publishedYear: req.body.publishedYear || "No year"
    };
    try {
        books.push(newBook);
        res.status(201).json(newBook);
    } catch (error) {
        res.status(500).json({ message: "Error creating book" });
    };
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});