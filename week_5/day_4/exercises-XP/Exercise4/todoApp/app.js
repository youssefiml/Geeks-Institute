import { TodoList } from "./todo.js";

const myTodos = new TodoList();

myTodos.addTask("Finish homework");
myTodos.addTask("Buy groceries");
myTodos.listTasks();

myTodos.completeTask(0);
myTodos.listTasks();