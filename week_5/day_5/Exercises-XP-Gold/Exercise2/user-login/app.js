import express from 'express';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';

const app = express();
app.use(express.json());

const PORT = 5000;
const users = [];
const SECRET_KEY = 'mySecretKey';

app.post('/api/register', async (req, res) => {
    const { email, password } = req.body;
    const hashedPassword = await bcrypt.hash(password, 10);

    const exist = users.find(u => u.email === email);
    if (exist) return res.status(400).json({ message: "User already exists" });

    users.push({ email, password: hashedPassword });

    res.json({ message: 'User registered successfully' });
});

app.post('/api/login', async (req, res) => {
    const { email, password } = req.body;

    const user = users.find(u => u.email === email);
    if (!user) {
        return res.status(401).json({ message: 'Invalid credentials' });
    }

    const isPasswordValid = await bcrypt.compare(password, user.password);
    if (!isPasswordValid) {
        return res.status(401).json({ message: 'Invalid credentials' });
    }

    const token = jwt.sign({ email: user.email }, SECRET_KEY, { expiresIn: '1h' });
    res.json({message: 'Login successful', token });
});

function auth(req, res, next) {
    const authHeader = req.headers.authorization;
    const token = authHeader && authHeader.split(" ")[1];

    if (!token) {
        return res.status(401).json({ message: 'Unauthorized' });
    }

    try {
        const decoded = jwt.verify(token, SECRET_KEY);
        req.user = decoded;
        next();
    } catch (error) {
        return res.status(401).json({ message: 'Unauthorized' });
    }
}

app.get("/api/profile", auth, (req, res) => {
    res.json({ message: "Profile data", user: req.user });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}/api/register`);
});