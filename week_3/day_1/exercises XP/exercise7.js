const names = ["Jack", "Philip", "Sarah", "Amanda", "Bernard", "Kyle"];
const societyName = [];

for (let name = 0; name < names.length; name++) {
    societyName.push(names[name][0]);
}

console.log(societyName.sort().join(''));