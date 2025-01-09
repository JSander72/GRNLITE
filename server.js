// filepath: /path/to/your/server.js
const express = require('express');
const jwt = require('jsonwebtoken');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');

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

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});