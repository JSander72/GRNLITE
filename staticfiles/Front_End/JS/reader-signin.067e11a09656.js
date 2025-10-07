document.getElementById("authForm").addEventListener("submit", function (e) {
    e.preventDefault();

    // Ensure the user type is 'reader'
    if (!selectedUserType || selectedUserType !== "reader") {
        alert("Please select 'Reader' as your role.");
        return;
    }

    // Redirect to Auth0 for reader sign-in
    const auth0Url = `https://dev-jkea1trp7tro4adh.us.auth0.com/authorize?response_type=code&client_id=YltoeNqyw0gcTm4ToOaIIvkUqJZ2VDkh&redirect_uri=${window.location.origin}/reader-dashboard.html&scope=openid profile email&state=reader`;
    window.location.href = auth0Url;
});

function initiateOAuth(provider) {
    if (!selectedUserType || selectedUserType !== "reader") {
        alert("Please select 'Reader' as your role.");
        return;
    }

    // Redirect to Auth0 OAuth for specific provider
    const auth0Url = `https://dev-jkea1trp7tro4adh.us.auth0.com/authorize?response_type=code&client_id=YltoeNqyw0gcTm4ToOaIIvkUqJZ2VDkh&connection=${provider}&redirect_uri=${window.location.origin}/reader-dashboard.html&scope=openid profile email&state=reader`;
    window.location.href = auth0Url;
}

