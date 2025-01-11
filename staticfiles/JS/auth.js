const AUTHO_CLIENT_ID = 'YltoeNqyw0gcTm4ToOaIIvkUqJZ2VDkh'; // Replace with your actual client ID

function initiateOAuth(provider, redirectUri) {
    let oauthUrl = '';
    const clientId = AUTHO_CLIENT_ID; // Replace with your actual client ID

    switch (provider) {
        case 'auth0':
            oauthUrl = `https://dev-jkea1trp7tro4adh.us.auth0.com/authorize?response_type=code&client_id=${clientId}&redirect_uri=${redirectUri}`;
            break;
        case 'google':
            oauthUrl = `https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=${clientId}&redirect_uri=${redirectUri}&scope=openid%20email%20profile`;
            break;
        case 'github':
            oauthUrl = `https://github.com/login/oauth/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&scope=user:email`;
            break;
        case 'facebook':
            oauthUrl = `https://www.facebook.com/v10.0/dialog/oauth?client_id=${clientId}&redirect_uri=${redirectUri}&scope=email`;
            break;
        case 'provider':
            console.error('Provider not implemented yet:', provider);
            return;  // Or handle not-implemented providers differently
        case 'token':
        case 'user':
            console.warn('initiateOAuth not intended for token or user endpoints');
            // Handle token or user logic differently in your application
            return;
        default:
            console.error('Unsupported OAuth provider:', provider);
            return;
    }

    // Redirect the user to the OAuth URL
    window.location.href = oauthUrl;
}

// Example usage
const provider = 'google'; // Replace with the desired provider
const redirectUri = 'https://yourapp.com/callback'; // Replace with your actual redirect URI
initiateOAuth(provider, redirectUri);
