const chalk = require('chalk');

function displayColorfulMessage() {
  console.log(chalk.blue.bold('║') + chalk.green('  Welcome to Node.js Development!  ') + chalk.blue.bold('║'));
  console.log(chalk.yellow('This is a ') + chalk.red.bold('colorful') + chalk.yellow(' message!'));
  console.log(chalk.cyan('Made with ❤️  using Chalk'));
}

module.exports = { displayColorfulMessage };