// Check authentication status and update nav links
async function checkAuth() {
    try {
        const response = await fetch('/api/profile/me');
        if (response.ok) {
            const user = await response.json();
            updateNavForLoggedIn(user);
            return user;
        } else {
            updateNavForLoggedOut();
            return null;
        }
    } catch (err) {
        updateNavForLoggedOut();
        return null;
    }
}

function updateNavForLoggedIn(user) {
    const navLinks = document.getElementById('navLinks');
    if (navLinks) {
        navLinks.innerHTML = `
            <a href="/profile/${user.username}" class="btn-link">My Profile</a>
            <a href="#" id="logoutBtn" class="btn-link">Logout</a>
        `;
        
        const logoutBtn = document.getElementById('logoutBtn');
        logoutBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            await logout();
        });
    }
}

function updateNavForLoggedOut() {
    const navLinks = document.getElementById('navLinks');
    if (navLinks) {
        navLinks.innerHTML = `
            <a href="/login" class="btn-link">Login</a>
            <a href="/signup" class="btn-primary">Sign Up</a>
        `;
    }
}

async function logout() {
    try {
        await fetch('/api/auth/logout', { method: 'POST' });
        window.location.href = '/';
    } catch (err) {
        console.error('Logout error:', err);
    }
}

// Run on page load
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
});
