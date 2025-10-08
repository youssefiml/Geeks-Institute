import express from "express";

const about = express.Router();

about.get('/', (req, res) => {
    res.send("About Youssef!");
});

export default about;