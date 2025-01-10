import { Pool } from 'pg';

const pool = new Pool({
    user: process.env.DB_USER,
    host: process.env.DB_HOST,
    database: process.env.DB_NAME,
    password: process.env.DB_PASSWORD,
    port: process.env.DB_PORT || 5432,
});

async function saveOAuthUserToDatabase(oauthProvider, accessToken, profileData) {
    const client = await pool.connect();
    try {
        const query = `INSERT INTO users (email, name, oauth_provider, access_token) 
                       VALUES ($1, $2, $3, $4)
                       ON CONFLICT (email) DO UPDATE
                       SET oauth_provider = $3, access_token = $4`;
        const values = [profileData.email, profileData.name, oauthProvider, accessToken];
        await client.query(query, values);
    } catch (err) {
        console.error('Error saving OAuth user:', err);
        throw new Error('Database operation failed');
    } finally {
        client.release();
    }
}

async function handleOAuthCallback() {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get("token");
    const userType = urlParams.get("userType");

    if (token) {
        try {
            // Display a loading spinner or message
            document.body.innerHTML = "<h2>Authenticating... Please wait.</h2>";

            localStorage.setItem("accessToken", token);

            // Fetch user data from OAuth provider
            const profileData = await fetchUserProfile(token);

            // Validate profile data
            if (!profileData.email || !profileData.name) {
                throw new Error('Invalid profile data');
            }

            // Save user to database
            await saveOAuthUserToDatabase(userType, token, profileData);

            // Redirect to the appropriate page
            window.location.href = "/dashboard";
        } catch (err) {
            console.error('Error during OAuth callback:', err);
            alert("Authentication failed. Please try again.");
            window.location.href = "/login";
        }
    } else {
        alert("Missing access token.");
        window.location.href = "/login";
    }
}

async function fetchUserProfile(token) {
    try {
        const response = await fetch('https://api.example.com/user', {
            headers: { Authorization: `Bearer ${token}` },
        });

        if (!response.ok) {
            throw new Error('Failed to fetch user profile');
        }

        return await response.json();
    } catch (err) {
        console.error('Error fetching user profile:', err);
        throw new Error('Failed to fetch profile data');
    }
}

// Call handleOAuthCallback when the page loads
window.onload = handleOAuthCallback;
