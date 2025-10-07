const express = require('express');
const app = express();
const { auth } = require('express-oauth2-jwt-bearer');
const port = process.env.PORT || 8080;

// Auth0 Configuration
const jwtCheck = auth({
  audience: 'this-is-grnlite-project-api',  // Auth0 API Audience
  issuerBaseURL: 'https://dev-3zzyd33uzb338uth.us.auth0.com/',  // Auth0 Domain
  tokenSigningAlg: 'RS256'
});

// Enforce JWT validation on all endpoints (or specify routes)
app.use(jwtCheck);

// API Routes
app.get('/authorized', (req, res) => {
  res.send('Secured Resource');
});

// Start the server
app.listen(port, () => {
  console.log('Server listening on port', port);
});