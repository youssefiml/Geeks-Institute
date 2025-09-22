const gameInfo = [
  {
    username: "john",
    team: "red",
    score: 5,
    items: ["ball", "book", "pen"]
  },
  {
    username: "becky",
    team: "blue",
    score: 10,
    items: ["tape", "backpack", "pen"]
  },
  {
    username: "susy",
    team: "red",
    score: 55,
    items: ["ball", "eraser", "pen"]
  },
  {
    username: "tyson",
    team: "green",
    score: 1,
    items: ["book", "pen"]
  },
];

const usernames = [];
const winners = [];
let totalScore = 0;

gameInfo.forEach(player => {
    usernames.push(player.username + "!");
    if (player.score > 5) {
      winners.push(player.username);
    }
    totalScore += player.score;
});

console.log("Usernames:", usernames);
console.log("Winners:", winners);
console.log("Total Score:", totalScore);
