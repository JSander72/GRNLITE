// import auth from './auth.js';
// import { initiateOAuth } from './auth.js';

function initiateOAuth(provider) {
    console.log('OAuth initiated with provider:', provider);
    // ...existing code...
}

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('signupForm');
    form.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevent the default form submission
        // Your code to handle form submission
        console.log('Form submitted');
        // Example: Access form values
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        console.log('Email:', email);
        console.log('Password:', password);
        // Add your form submission logic here
        alert('Form submitted successfully!');
    });
});
