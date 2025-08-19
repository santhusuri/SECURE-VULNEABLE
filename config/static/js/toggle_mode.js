/**
 * Toggle Mode Script
 * -------------------
 * Handles switching between Secure Mode and Vulnerable Mode.
 * Updates button UI + label, and makes a POST request to Django
 * (`/accounts/toggle_mode/`) to update session state.
 */

// ================= Toggle Mode Script =================

// Grab DOM elements
const toggleBtn = document.getElementById('toggle-mode-btn');
const vulnLabel = document.getElementById('vuln-label');

// Get context variables from Django (passed in base.html)
let currentMode = window.APP_CONTEXT.mode || "secure";
const csrfToken = window.APP_CONTEXT.csrfToken || "";

/**
 * Update the button + label UI based on mode
 */
function updateButtonUI(mode) {
    if (mode === "vulnerable") {
        toggleBtn.textContent = "Vulnerable Mode";
        toggleBtn.style.backgroundColor = "#dc3545"; // red
        toggleBtn.style.color = "#fff";
        vulnLabel.style.display = "inline-block";   // show label
    } else {
        toggleBtn.textContent = "Secure Mode";
        toggleBtn.style.backgroundColor = "#ffc107"; // yellow
        toggleBtn.style.color = "#000";
        vulnLabel.style.display = "none";           // hide label
    }
}

// Initial UI setup
updateButtonUI(currentMode);

// Click listener to toggle mode
toggleBtn.addEventListener('click', function () {
    fetch('/accounts/toggle_mode/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if (data.mode) {
            currentMode = data.mode;
            updateButtonUI(currentMode);

            // Redirect to login page when mode changes
            if (currentMode === "vulnerable") {
                alert("Switched to Vulnerable Mode! Redirecting to login page for labs.");
            } else {
                alert("Switched to Secure Mode!");
            }
            window.location.href = "/accounts/login/";
        }
    })
    .catch(() => {
        alert("⚠️ Error toggling mode!");
    });
});
