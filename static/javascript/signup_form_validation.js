/* Signup Form Validation scripts */
// Get DOM elements
const usernameInput = document.getElementById("username");
const usernameErrorMessage = document.getElementById("username-error-message");

const emailInput = document.getElementById("email");
const emailErrorMessage = document.getElementById("email-error-message");

const passwordInput = document.getElementById("password");
const passwordErrorMessage = document.getElementById("password-error-message");


// Listeners for DOM elements
usernameInput.addEventListener("input", function() {
  usernameErrorMessage.style=""
  if (usernameInput.value.length >= 8) {
    usernameErrorMessage.textContent = ""; // clear error message if email is valid
    check_database_for_username(usernameInput.value)
  } else {
    usernameErrorMessage.textContent = "Username must be 8 or more characters";
  }
});


emailInput.addEventListener("input", function() {
  emailErrorMessage.style=""
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (emailPattern.test(emailInput.value)) {
    emailErrorMessage.textContent = ""; // clear error message if email is valid
    check_database_for_email(emailInput.value)
  } else {
    emailErrorMessage.textContent = "Please enter a valid email address";
  }
});


passwordInput.addEventListener("input", function() {
  passwordErrorMessage.style=""
    let passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\da-zA-Z]).{8,}$/;
  if (passwordRegex.test(passwordInput.value)) {
    passwordErrorMessage.textContent = ""; // clear error message if email is valid
  } else {
    passwordErrorMessage.textContent = "Password must be at least 8 characters long and include a minimum of uppercase, lowercase, number, and symbol";
  }
});


// Database queries for unique values
function check_database_for_username(username) {
    fetch(`/check_username?username=${encodeURIComponent(username)}`)
    .then(response => response.json())
    .then(data => {
      if (data.exists) {
        usernameErrorMessage.textContent = "That username is already taken";
        usernameErrorMessage.style = 'background-color: yellow;'
      } else {
        usernameErrorMessage.textContent = "";
      }
    });
}

function check_database_for_email(email) {
    fetch(`/check_email?email=${encodeURIComponent(email)}`)
    .then(response => response.json())
    .then(data => {
      if (data.exists) {
        emailErrorMessage.textContent = "Email is already in use";
        emailErrorMessage.style = 'background-color: yellow;'
      } else {
        emailErrorMessage.textContent = "";
      }
    });
}
