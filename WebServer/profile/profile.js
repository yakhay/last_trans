
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("btn").onclick = function() {
        document.getElementById("avatarForm").style.display = "block";
        get_csrf_token1();
    };
    document.getElementById("usernameBtn").onclick = function() {
        document.getElementById("userform").style.display = "block";
        get_csrf_token();
    };
    getProfile();
});

function get_csrf_token1(){
    fetch('/api/csrf-token/')
    .then(response => response.json())
    .then(data => {
        document.getElementById('csrfToken1').value = data.csrfToken;
    })
    .catch(error => console.error('Error fetching CSRF token:', error));
}

function get_csrf_token(){
    fetch('/api/csrf-token/')
    .then(response => response.json())
    .then(data => {
        document.getElementById('csrfToken').value = data.csrfToken;
    })
    .catch(error => console.error('Error fetching CSRF token:', error));
}

function getProfile() {
    fetch('/api/data/')
    .then(response => {
        if (!response.ok) {
            window.location.href = "/";
        }
        return response.json();
    })
    .then(data => {
        const userData = JSON.parse(JSON.stringify(data));
        document.getElementById("avatar").src = userData.photo_profile;
        document.getElementById("username").innerHTML = userData.username;
        console.log(userData);
    })
}

