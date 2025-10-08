
import { Book } from "../models/index.js";

const getbooks=async(req,res)=>{
    const books=await Book.findAll();
    res.json(books);
};
const getbook=async(req,res)=>{
    const id=req.params.id;
    const book=await Book.findByPk(id);
    res.json(book);
};
const createbook=async(req,res)=>{
    const data=req.body;
    await Book.create(data);
    res.send('book created success ');
};
const updatebook=async(req,res)=>{
    const id=req.params.id;
        const data=req.body;
    await Book.update(data, { where: { id } });
    res.send('book updated success ');
}
const deletebook=async(req,res)=>{
    const id=req.params.id;
    await Book.destroy( { where: { id } });
    res.send('book deleted success ');
}
module.exports={deletebook,updatebook,createbook,getbook,getbooks};