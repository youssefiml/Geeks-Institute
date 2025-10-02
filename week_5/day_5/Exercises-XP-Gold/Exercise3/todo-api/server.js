import express from 'express';

const app = express();
const PORT = 3000;


let todos = [];

app.use(express.json());

app.post('/api/todos', (req, res) => {
    const todo = req.body;

    if (!todo.title) {
        return res.status(400).json({ message: "Todo title is required" });
    };

    const newTodo = {id: todos.length + 1,
        title: todo.title, 
        completed: todo.completed === true
    };

    todos.push(newTodo);
    res.status(201).json(newTodo);
});

app.get('/api/todos', (req, res) => {
    res.json(todos);
});

app.get('/api/todos/:id', (req, res) => {
    const todoId = parseInt(req.params.id, 10);

    const todo = todos.find(t => t.id === todoId);

    if (todo) {
        res.json(todo);
    } else {
        res.status(404).json({ message: 'Todo not found' });
    }
});

app.put('/api/todos/:id', (req, res) => {
    const todoId = parseInt(req.params.id, 10);
    if (isNaN(todoId)) {
    return res.status(400).json({ message: "Invalid ID" });
    }

    const todo = todos.find(t => t.id === todoId);
    if (todo) {
        todo.title = req.body.title;
        todo.completed = req.body.completed === true;
        res.json(todo);
    } else {
        res.status(404).json({ message: 'Todo not found' });
    }
});

app.delete('/api/todos/:id', (req, res) => {
    const todoId = parseInt(req.params.id, 10);

    if (isNaN(todoId)) {
        return res.status(400).json({ message: "Invalid ID" });
    }

    const todoIndex = todos.findIndex(t => t.id === todoId);

    if (todoIndex === -1) {
        return res.status(404).json({ message: 'Todo not found' });
    }

    todos.splice(todoIndex, 1)[0];
    res.json({ message: 'Todo deleted successfully' });
});


app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}/api/todos`);
});