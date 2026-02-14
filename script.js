// Function to Open Modals
function openModal(modalId) {
    document.getElementById(modalId).style.display = 'flex';
}

// Function to Close Modals
function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Close Modal if clicking outside content
window.onclick = function(event) {
    if (event.target.classList.contains('modal-overlay')) {
        event.target.style.display = "none";
    }
}

// Confirm Delete Alert
function confirmDelete() {
    return confirm("Are you sure you want to permanently delete this post?");
}