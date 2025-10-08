import express from "express";

const home = express.Router();

home.get('/', (req, res) => {
    res.send("Hello World!");
});

export default home;