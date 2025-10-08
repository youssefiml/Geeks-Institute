import express from "express";
import fs from "fs";

const app = express();
const PORT = 3000;
const FILE_PATH = "./tasks.json";

app.use(express.json());

app.get("/tasks", (req, res) => {
  try {
    const data = fs.readFileSync(FILE_PATH, "utf8");
    const tasks = JSON.parse(data);
    res.json(tasks);
  } catch (err) {
    res.status(500).json({ message: "Error reading tasks file" });
  }
});

app.get("/tasks/:id", (req, res) => {
  try {
    const data = fs.readFileSync(FILE_PATH, "utf8");
    const tasks = JSON.parse(data);
    const task = tasks.find(t => t.id === parseInt(req.params.id));

    if (!task) {
      return res.status(404).json({ message: "Task not found" });
    }

    res.json(task);
  } catch (err) {
    res.status(500).json({ message: "Error reading tasks file" });
  }
});

app.post("/tasks", (req, res) => {
  try {
    const { title, description } = req.body;

    if (!title || !description) {
      return res.status(400).json({ message: "Title and description are required" });
    }

    const data = fs.readFileSync(FILE_PATH, "utf8");
    const tasks = JSON.parse(data);

    const newTask = {
      id: tasks.length ? tasks[tasks.length - 1].id + 1 : 1,
      title,
      description,
    };

    tasks.push(newTask);
    fs.writeFileSync(FILE_PATH, JSON.stringify(tasks, null, 2));

    res.status(201).json(newTask);
  } catch (err) {
    res.status(500).json({ message: "Error writing to tasks file" });
  }
});

app.put("/tasks/:id", (req, res) => {
  try {
    const { title, description } = req.body;
    const data = fs.readFileSync(FILE_PATH, "utf8");
    const tasks = JSON.parse(data);
    const taskIndex = tasks.findIndex(t => t.id === parseInt(req.params.id));

    if (taskIndex === -1) {
      return res.status(404).json({ message: "Task not found" });
    }

    if (!title && !description) {
      return res.status(400).json({ message: "Nothing to update" });
    }

    if (title) tasks[taskIndex].title = title;
    if (description) tasks[taskIndex].description = description;

    fs.writeFileSync(FILE_PATH, JSON.stringify(tasks, null, 2));

    res.json(tasks[taskIndex]);
  } catch (err) {
    res.status(500).json({ message: "Error updating task" });
  }
});

app.delete("/tasks/:id", (req, res) => {
  try {
    const data = fs.readFileSync(FILE_PATH, "utf8");
    let tasks = JSON.parse(data);
    const newTasks = tasks.filter(t => t.id !== parseInt(req.params.id));

    if (tasks.length === newTasks.length) {
      return res.status(404).json({ message: "Task not found" });
    }

    fs.writeFileSync(FILE_PATH, JSON.stringify(newTasks, null, 2));
    res.json({ message: "Task deleted successfully" });
  } catch (err) {
    res.status(500).json({ message: "Error deleting task" });
  }
});

app.get("/", (req, res) => {
  res.send("Task Management API is running");
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});

