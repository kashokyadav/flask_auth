// SIGNUP
const signupForm = document.getElementById("signupform");

if (signupForm) {

    signupForm.addEventListener("submit", async (e) => {

        e.preventDefault();

        const data = {
            name: document.getElementById("name").value,
            email: document.getElementById("email").value,
            password: document.getElementById("password").value
        };

        const response = await fetch("/", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.status === "success") {

            window.location.href = '/login';

        } else {

            document.getElementById("error").textContent =
                result.message;
        }
    });
}




// LOGIN
const loginForm = document.getElementById("loginform");

if (loginForm) {

    loginForm.addEventListener("submit", async (e) => {

        e.preventDefault();

        const data = {
            email: document.getElementById("email").value,
            password: document.getElementById("password").value
        };

        const response = await fetch("/login", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.status === "success") {

            window.location.href = '/home';

        } else {

            document.getElementById("error").textContent =
                result.message;
        }
    });
}