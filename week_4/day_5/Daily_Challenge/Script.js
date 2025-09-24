function isAnagram(str1, str2) {
  const formatString = (str) =>
    str.toLowerCase().replace(/\s+/g, '').split('').sort().join('');

  return formatString(str1) === formatString(str2);
}

// Test Cases
console.log(isAnagram("Astronomer", "Moon starer"));        // ➞ true
console.log(isAnagram("School master", "The classroom"));   // ➞ true
console.log(isAnagram("The Morse Code", "Here come dots")); // ➞ true
console.log(isAnagram("Hello", "World"));                   // ➞ false