let guestList = {
  randy: "Germany",
  karla: "France",
  wendy: "Japan",
  norman: "England",
  sam: "Argentina"
}

userName = prompt("Enter your name").toLowerCase();

if (userName in guestList) {
    console.log("Hi! I'm " + userName + ", and I'm from " + guestList[userName]);
} else {
    console.log("Hi! I'm a guest.");
}