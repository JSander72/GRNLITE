document.getElementById("authForm").addEventListener("submit", function (e) {
    e.preventDefault();

    // Ensure the user type is 'author'
    if (!selectedUserType || selectedUserType !== "author") {
        alert("Please select 'Author' as your role.");
        return;
    }

    // Redirect to Auth0 for author sign-in
    const auth0Url = `https://dev-jkea1trp7tro4adh.us.auth0.com/authorize?response_type=code&client_id=YltoeNqyw0gcTm4ToOaIIvkUqJZ2VDkh&redirect_uri=${window.location.origin}/author-dashboard.html&scope=openid profile email&state=author`;
    window.location.href = auth0Url;
});

function initiateOAuth(provider) {
    if (!selectedUserType || selectedUserType !== "author") {
        alert("Please select 'Author' as your role.");
        return;
    }

    // Redirect to Auth0 OAuth for specific provider
    const auth0Url = `https://dev-jkea1trp7tro4adh.us.auth0.com/authorize?response_type=code&client_id=YltoeNqyw0gcTm4ToOaIIvkUqJZ2VDkh&connection=${provider}&redirect_uri=${window.location.origin}/author-dashboard.html&scope=openid profile email&state=author`;
    window.location.href = auth0Url;
}

