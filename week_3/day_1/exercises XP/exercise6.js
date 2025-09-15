const details = {
  my: 'name',
  is: 'Rudolf',
  the: 'reindeer'
}
let sentence = '';
for (let value in details) {
    sentence += value + ' ' + details[value] + ' ';
}
console.log(sentence.trim());