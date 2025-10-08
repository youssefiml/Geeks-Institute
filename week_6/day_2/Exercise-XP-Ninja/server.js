import express from "express";
import path from "path";
import greetRoutes from "./routes/greet.routes.js";

const app = express();
const PORT = 3000;

app.use(express.urlencoded({ extended: true }));
app.use(express.static("public"));

app.use("/", greetRoutes);

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
}); 