document.getElementById("authForm").addEventListener("submit", function (e) {
    e.preventDefault();

    // Ensure the user type is 'author'
    if (!selectedUserType || selectedUserType !== "author") {
        alert("Please select 'Author' as your role.");
        return;
    }

    // Submit the form to Django's built-in authentication system
    const form = e.target;
    const formData = new FormData(form);

    fetch('/login/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/author-dashboard/';
        } else {
            alert('Login failed: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
