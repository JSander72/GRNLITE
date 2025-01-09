

function initiateOAuth(provider) {
    let oauthUrl = '';

    switch (provider) {
        case 'auth0':
            oauthUrl = 'https://dev-jkea1trp7tro4adh.us.auth0.com/authorize';
            break;
        case 'provider':
            oauthUrl = 'https://dev-jkea1trp7tro4adh.us.auth0.com/authorize';
            break;
        case 'token':
            oauthUrl = 'https://dev-jkea1trp7tro4adh.us.auth0.com/oauth/token';
            break;
        case 'user':
            oauthUrl = 'https://dev-jkea1trp7tro4adh.us.auth0.com/userinfo';
            break;
    
        default:
            console.error('Unsupported OAuth provider');
            return;
    }

    // Redirect to the OAuth provider's URL
    window.location.href = oauthUrl;
}