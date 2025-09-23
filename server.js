// filepath: /path/to/your/server.js
const express = require('express');
const jwt = require('jsonwebtoken');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const keepAliveService = require('./keepAlive');

const app = express();
const port = 3000;

app.use(bodyParser.json());
app.use(cookieParser());

const JWT_SECRET = 'YOUR_JWT_SECRET';
const JWT_REFRESH_SECRET = 'YOUR_JWT_REFRESH_SECRET';

// In-memory storage for CSRF tokens (use a database in production)
const csrfTokens = {};

function generateTokens(user) {
    const accessToken = jwt.sign(user, JWT_SECRET, { expiresIn: '15m' });
    const refreshToken = jwt.sign(user, JWT_REFRESH_SECRET, { expiresIn: '7d' });
    return { accessToken, refreshToken };
}

app.post('/api/create-account', (req, res) => {
    const token = req.headers.authorization.split(' ')[1];
    const decoded = jwt.verify(token, JWT_SECRET);

    // Create account in the database
    const user = {
        id: decoded.id,
        username: decoded.username,
        userType: req.body.userType,
        token: token  // Store the token in the database
    };

    // Save user to database (pseudo code)
    // database.saveUser(user);

    const tokens = generateTokens(user);
    res.cookie('refreshToken', tokens.refreshToken, { httpOnly: true });
    res.status(201).send({ accessToken: tokens.accessToken, message: 'Account created' });
});

app.post('/api/refresh-token', (req, res) => {
    const refreshToken = req.cookies.refreshToken;
    if (!refreshToken) return res.sendStatus(401);

    jwt.verify(refreshToken, JWT_REFRESH_SECRET, (err, user) => {
        if (err) return res.sendStatus(403);
        const tokens = generateTokens(user);
        res.cookie('refreshToken', tokens.refreshToken, { httpOnly: true });
        res.json({ accessToken: tokens.accessToken });
    });
});

// Endpoint to store CSRF token
app.post('/store-csrf-token', (req, res) => {
    const { csrfToken } = req.body;
    if (csrfToken) {
        // Store the CSRF token (use a database in production)
        csrfTokens[csrfToken] = true;
        res.status(200).send('CSRF token stored');
    } else {
        res.status(400).send('CSRF token missing');
    }
});

// Endpoint to retrieve CSRF token (if needed)
app.get('/retrieve-csrf-token/:token', (req, res) => {
    const csrfToken = req.params.token;
    if (csrfTokens[csrfToken]) {
        res.status(200).send('CSRF token valid');
    } else {
        res.status(404).send('CSRF token not found');
    }
});

const router = express.Router();
const Token = require('../models/Token'); // Assuming you have a Token model

router.get('/verify-token', async (req, res) => {
    const token = req.query.token;
    try {
        const tokenRecord = await Token.findOne({ token: token });
        if (tokenRecord) {
            res.status(200).json({ exists: true });
        } else {
            res.status(404).json({ exists: false });
        }
    } catch (error) {
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// Health check endpoint for keep-alive service
app.get('/api/health-check', (req, res) => {
    const stats = keepAliveService.getStats();
    res.status(200).json({
        status: 'OK',
        timestamp: new Date().toISOString(),
        uptime: process.uptime(),
        keepAlive: stats,
        message: 'Server is running and healthy'
    });
});

// Status endpoint to check keep-alive service
app.get('/api/keep-alive-status', (req, res) => {
    const stats = keepAliveService.getStats();
    res.status(200).json({
        keepAliveService: stats
    });
});

app.use('/api', router);

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
    
    // Start the keep-alive service only in production
    if (process.env.NODE_ENV === 'production' || process.env.RENDER_EXTERNAL_URL) {
        console.log('🔄 Starting keep-alive service for production...');
        keepAliveService.start();
    } else {
        console.log('⚠️  Keep-alive service disabled in development mode');
        console.log('   Set NODE_ENV=production or RENDER_EXTERNAL_URL to enable');
    }
});