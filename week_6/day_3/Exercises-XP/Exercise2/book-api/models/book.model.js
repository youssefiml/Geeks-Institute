import { DataTypes } from "sequelize";
import sequelize from "../config/db.js";

const Book = sequelize.define('book', {
  id: {
    type: DataTypes.INTEGER,
    autoIncrement: true,
    primaryKey: true,
    allowNull: false
  },
  title: {
    type: DataTypes.STRING,
    allowNull: false
  },
  author: {
    type: DataTypes.STRING,
    allowNull: false
  },
  publishedYear: {
    type: DataTypes.DATEONLY,  // مهم باش يتوافق مع جدولك
    allowNull: false,
    field: 'publishedYear'
  }
}, {
  tableName: 'books',
  timestamps: false
});

export default Book;