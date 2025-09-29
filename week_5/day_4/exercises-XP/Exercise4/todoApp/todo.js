export class TodoList {
  constructor() {
    this.tasks = [];
  }

  addTask(description) {
    this.tasks.push({
      description,
      completed: false
    });
    console.log(`Task added: "${description}"`);
  }

  completeTask(index) {
    if (index < 0 || index >= this.tasks.length) {
      console.log("Invalid task index");
      return;
    }
    this.tasks[index].completed = true;
    console.log(`Task completed: "${this.tasks[index].description}"`);
  }

  listTasks() {
    if (this.tasks.length === 0) {
      console.log("No tasks available.");
      return;
    }

    console.log("Todo List:");
    this.tasks.forEach((task, i) => {
      console.log(`${i + 1}. [${task.completed ? "✔" : " "}] ${task.description}`);
    });
  }
}
