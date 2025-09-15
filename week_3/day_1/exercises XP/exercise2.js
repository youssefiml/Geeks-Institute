const colors = ['purple', 'red', 'green', 'yellow', 'white'];

for (let i = 0; i < colors.length; i++) {
    console.log(`My #${i + 1} choice is ${colors[i]}`);
}

const suffixes = ['st', 'nd', 'rd', 'th', 'th'];

for (let i = 0; i < colors.length; i++) {
    const suffix = suffixes[i] || 'th';
    console.log(`My ${i + 1}${suffix} choice is ${colors[i]}`);
}