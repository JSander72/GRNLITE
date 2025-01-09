// filepath: /path/to/your/server.js
const express = require('express');
const jwt = require('jsonwebtoken');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

app.post('/api/create-account', (req, res) => {
    const token = req.headers.authorization.split(' ')[1];
    const decoded = jwt.verify(token, 'YOUR_JWT_SECRET');

    // Create account in the database
    const user = {
        id: decoded.id,
        username: decoded.username,
        userType: req.body.userType
    };

    // Save user to database (pseudo code)
    // database.saveUser(user);

    res.status(201).send({ message: 'Account created' });
});

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});