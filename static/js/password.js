function togglePassword() {
    var passwordInput = document.getElementById("new_password");
    var confpass = document.getElementById("conf_password");
    
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    }

    if (confpass.type === "password") {
        confpass.type = "text";
    } else {
        confpass.type = "password";
    }

}