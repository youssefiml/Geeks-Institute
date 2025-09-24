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
        if (morse) {
            const morseJs = JSON.parse(morse);
            resolve(morseJs);
        } else {
            reject('There is no morse code');
        }
    });
}

function toMorse(morseJs) {
    return new Promise((resolve, reject) => {
        const text = 'sos';             
        const textToMorse = [];
        text.split('').forEach(letter => {
            if (morseJs[letter]) {
                textToMorse.push(morseJs[letter]);
            }
        });
        if (textToMorse.length > 0) {
            resolve(textToMorse.join(' '));
        } else {
            reject('The morse code is empty');
        }   
    });
}

function joinWords(morseTranslation) {
    return new Promise((resolve, reject) => {
        if (morseTranslation) {
            resolve(morseTranslation);
        } else {
            reject('There is no morse translation');
        }
    }); 
}

console.log(joinWords())