const users = { 
    user1: 18273, 
    user2: 92833, 
    user3: 90315 
};

// Part 1
const usersArray = Object.entries(users);
console.log("Part 1 Output:", usersArray);

// Part 2
const updatedUsersArray = usersArray.map(([key, value]) => [key, value * 2]);
console.log("Part 2 Output:", updatedUsersArray);
