document.addEventListener("DOMContentLoaded", function(){
    const passwordInput = document.querySelector("input[name='password']");
    const usernameInput = document.querySelector("input[name='username']");

    passwordInput.addEventListener("focus", function(){
        console.log("Hint: Try SQL injection like ' OR '1'='1' -- ");
    });
});
