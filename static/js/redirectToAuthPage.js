function redirectToAuthPage(page) {
    // Use URLs for Django's built-in authentication system
    let url;
    if (page === 'signup') {
        url = '/accounts/signup/';
    } else if (page === 'signin') {
        url = '/accounts/login/';
    } else {
        console.error('Invalid page requested:', page);
        return;
    }

    // Redirect to the appropriate page
    window.location.href = url;
}