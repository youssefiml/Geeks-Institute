const morse = `{
  "0": "-----",
  "1": ".----",
  "2": "..---",
  "3": "...--",
  "4": "....-",
  "5": ".....",
  "6": "-....",
  "7": "--...",
  "8": "---..",
  "9": "----.",
  "a": ".-",
  "b": "-...",
  "c": "-.-.",
  "d": "-..",
  "e": ".",
  "f": "..-.",
  "g": "--.",
  "h": "....",
  "i": "..",
  "j": ".---",
  "k": "-.-",
  "l": ".-..",
  "m": "--",
  "n": "-.",
  "o": "---",
  "p": ".--.",
  "q": "--.-",
  "r": ".-.",
  "s": "...",
  "t": "-",
  "u": "..-",
  "v": "...-",
  "w": ".--",
  "x": "-..-",
  "y": "-.--",
  "z": "--..",
  ".": ".-.-.-",
  ",": "--..--",
  "?": "..--..",
  "!": "-.-.--",
  "-": "-....-",
  "/": "-..-.",
  "@": ".--.-.",
  "(": "-.--.",
  ")": "-.--.-"
}`


function toJs() {
    return new Promise((resolve, reject) => {
        try {
            const jsonString = JSON.parse(morse);
            if (Object.keys(jsonString).length === 0) {
                reject("Error: The object is empty");
            } else {
                resolve(jsonString);
            }
        } catch (error) {
            reject("Error: Could not convert to JSON string");
        }
    });
}
function toMorse(morseJS) {
    return new Promise((resolve, reject) => {
        const userInput = prompt("Enter a word or sentence:");
        const lowerCasedInput = userInput.toLowerCase();
        const inputArray = lowerCasedInput.split("");
        const morseTranslation = [];
        for (let char of inputArray) {
            if (morseJS[char]) {
                morseTranslation.push(morseJS[char]);
            } else if (char === " ") {
                morseTranslation.push(" / ");
            } else {
                reject(`Error: Character "${char}" cannot be translated to Morse code`);
                return;
            }
        }
        resolve(morseTranslation);
    });
}
function joinWords(morseTranslation) {
    const result = morseTranslation.join("\n");
    const pre = document.createElement("pre");
    pre.textContent = result;
    document.body.appendChild(pre);
}
toJs()
    .then(morseJS => toMorse(morseJS))
    .then(morseTranslation => joinWords(morseTranslation))
    .catch(error => alert(error))