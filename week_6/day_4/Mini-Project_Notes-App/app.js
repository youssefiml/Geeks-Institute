const fs = require("fs");
const yargs = require("yargs");
const { hideBin } = require("yargs/helpers");
const _ = require("lodash");
const notes = require("./notes");
const argv = yargs(hideBin(process.argv))
  .command({
    command: "add",
    describe: "Add a new note",
    builder: {
      title: {
        describe: "Note title",
        demandOption: true,
        type: "string",
      },
      body: {
        describe: "Note body",
        demandOption: true,
        type: "string",
      },
    },
    handler(argv) {
      notes.addNote(argv.title, argv.body);
    },
  })
  .command({
    command: "list",
    describe: "List all notes",
    handler() {
      notes.listNotes();
    },
  })
  .command({
    command: "read",
    describe: "Read a note",
    builder: {
      title: {
        describe: "Note title",
        demandOption: true,
        type: "string",
      },
    },
    handler(argv) {
      notes.readNote(argv.title);
    },
  })
  .command({
    command: "remove",
    describe: "Remove a note",
    builder: {
      title: {
        describe: "Note title",
        demandOption: true,
        type: "string",
      },
    },
    handler(argv) {
      notes.removeNote(argv.title);
    },
  })
  .demandCommand(1, "You need to specify a valid command.")
  .help()
  .parse();
