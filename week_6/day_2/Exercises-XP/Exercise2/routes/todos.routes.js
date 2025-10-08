import express from "express";

const todos = [
    {
        id: 1,
        name: "Todo 1"
    },
    {
        id: 2,
        name: "Todo 2"
    },
    {
        id: 3,
        name: "Todo 3"
    }
];

const router = express.Router();

router.get("/", (req, res) => {
    res.json(todos)
});

router.post("/", (req, res) => {
    const newTodo = {
        id: todos.length + 1,
        name: req.body.name
    };

    try {    
        todos.push(newTodo);
        res.status(201).json(newTodo);
    } catch (error) {
        res.status(500).json({ message: "Error creating todo" });
    };
})

router.put("/:id", (req, res) => {
    const todoId = parseInt(req.params.id, 10);
    const todo = todos.find(t => t.id === todoId);

    if (!todo) {
        return res.status(404).json({ message: "Todo not found" });
    }

    try {
        todo.name = req.body.name;
        res.json(todo);
    } catch (error) {
        res.status(500).json({ message: "Error updating todo" });
    }
});

router.delete("/:id", (req, res) => {
    const todoId = parseInt(req.params.id, 10);
    const todoIndex = todos.findIndex(t => t.id === todoId);

    if (todoIndex === -1) {
        return res.status(404).json({ message: "Todo not found" });
    }

    try {
        todos.splice(todoIndex, 1);
        res.json({ message: "Todo deleted successfully" });
    } catch (error) {
        res.status(500).json({ message: "Error deleting todo" });
    }
});

export default router;