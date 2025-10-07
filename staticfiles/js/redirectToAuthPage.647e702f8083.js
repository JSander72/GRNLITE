function redirectToAuthPage(page) {
    let url;
    if (page === 'signup') {
        url = '/signup/';
    } else if (page === 'signin') {
        url = '/signin/';
    } else {
        console.error('Invalid page requested:', page);
        return;
    }

    window.location.href = url;
}