let sentence = 'The weather today is not at all.'

let wordNot = sentence.indexOf("not")
let wordBad = sentence.indexOf("bad")
console.log(wordNot)
console.log(wordBad)
let newSentence = ""
if (wordBad > wordNot){
    newSentence = sentence.replace("not bad", "good")
} else {
    console.log(sentence)
}
console.log(newSentence)