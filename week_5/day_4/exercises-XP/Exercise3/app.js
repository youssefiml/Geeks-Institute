import { readFile, writeFile} from "./fileManager.js";

readFile("Hello World.txt", (err, data) => {
  if (err) {
    console.error("Error reading Hello World.txt:", err);
    return;
  }
  console.log("Content of Hello World.txt:", data);

writeFile("Bye World.txt", "Writing to the file", (err) => {
    if (err) {
      console.error("Error writing to Bye World.txt:", err);
    } else {
      console.log("Successfully wrote to Bye World.txt!");
    }
  });
});

