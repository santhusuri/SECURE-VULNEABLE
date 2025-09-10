/**
 * Toggle Mode Script
 * -------------------
 * Handles switching between Secure Mode and Vulnerable Mode.
 * Updates button UI + label, makes POST requests to Django endpoints,
 * and starts the attack simulation when switching to vulnerable mode.
 */

// ================= DOM Elements =================
const toggleBtn = document.getElementById('toggle-mode-btn');
const vulnLabel = document.getElementById('vuln-label');

// Context from Django (passed in base.html)
let currentMode = window.APP_CONTEXT.mode || "secure";
const csrfToken = window.APP_CONTEXT.csrfToken || "";

// ================= Update Button UI =================
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

// ================= Toggle Mode Handler =================
toggleBtn.addEventListener("click", () => {
    const newMode = currentMode === "secure" ? "vulnerable" : "secure";

    fetch("/core/toggle_mode/", {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ mode: newMode }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "ok") {
            currentMode = newMode;
            window.APP_CONTEXT.mode = newMode;
            updateButtonUI(newMode);

            // Start attack simulation automatically if vulnerable
            if (newMode === "vulnerable") {
                fetch("/core/start_attack_simulation/")
                    .then(res => res.json())
                    .then(resp => console.log(resp.status))
                    .catch(err => console.error("Attack simulation error:", err));
            }
        }
    })
    .catch(err => {
        console.error("Error toggling mode:", err);
        alert("⚠️ Failed to toggle mode!");
    });
});
