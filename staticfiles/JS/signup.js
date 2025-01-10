document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('signupForm');
    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent the default form submission
        // Your code to handle form submission
        console.log('Form submitted');
        // Example: Access form values
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        console.log('Email:', email);
        console.log('Password:', password);

        // Fetch the token from an API
        let token;
        try {
            const response = await fetch('/api/get-token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });
            const data = await response.json();
            token = data.token;
        } catch (error) {
            console.error('Error fetching token:', error);
            token = null;
        }

        console.log('Token:', token);
        // Add your form submission logic here
    });
});
