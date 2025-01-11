function redirectToAuthPage(page) {
    // Use URLs dynamically passed from Django template
    let url;
    if (page === 'signup') {
        url = signupUrl;
    } else if (page === 'signin') {
        url = signinUrl;
    } else {
        console.error('Invalid page requested:', page);
        return;
    }

    // Redirect to the appropriate page
    window.location.href = url;
}