import { Sequelize } from "sequelize";

const sequelize = new Sequelize('blog-api', 'postgres', '0000', {
    host: 'localhost',
    dialect: 'postgres',
});
const connectDB = async () => {
    try {
        await sequelize.authenticate();
        console.log("✅ Connected successfully");
    } catch (error) {
        console.error("❌ Unable to connect:", error);
    }
};

module.exports = { sequelize, connectDB };