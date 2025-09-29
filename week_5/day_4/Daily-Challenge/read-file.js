const fs = require('fs');
const path = require('path');

function readFileContent() {
  const filePath = path.join(__dirname, 'files', 'file-data.txt');
  
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    console.log('\n--- File Content ---');
    console.log(content);
    console.log('--- End of File ---\n');
    return content;
  } catch (error) {
    console.error('Error reading file:', error.message);
    return null;
  }
}

module.exports = { readFileContent };