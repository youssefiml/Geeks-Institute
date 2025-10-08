import express from "express";

const router = express.Router();

const books = [
    {
        id: 1,
        title: "python",
        author: "Guido van Rossum"
    },
    {
        id: 2,
        title: "java",
        author: "James Gosling"
    },
    {
        id: 3,
        title: "javascript",
        author: "Brendan Eich"
    }
];

router.get("/", (req, res) => {
    res.json(books);
});

router.post("/", (req, res) => {
    const newBook = {
        id: books.length + 1,
        title: req.body.title,
        author: req.body.author
    };

    books.push(newBook);
    res.json(newBook);
});

router.put("/:id", (req, res) => {
    const bookId = parseInt(req.params.id, 10);
    const book = books.find(b => b.id === bookId);

    if (book) {
        book.title = req.body.title || book.title;
        book.author = req.body.author || book.author;
        res.json(book);
    } else {
        res.status(404).json({ message: "Book not found" });
    }
});

router.delete("/:id", (req, res) => {
    const bookId = parseInt(req.params.id, 10);
    const bookIndex = books.findIndex(b => b.id === bookId);

    if (bookIndex !== -1) {
        books.splice(bookIndex, 1);
        res.json({ message: "Book deleted successfully" });
    } else {
        res.status(404).json({ message: "Book not found" });
    }
});

export default router;