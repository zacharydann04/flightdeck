let currentUser = null;

document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Fetch current user profile
        const response = await fetch('/api/profile/me');
        
        if (!response.ok) {
            // Not authenticated, redirect to login
            window.location.href = '/login';
            return;
        }
        
        currentUser = await response.json();
        
        // Update nav links
        document.getElementById('profileLink').href = `/profile/${currentUser.username}`;
        document.getElementById('profileLink').textContent = currentUser.username;
        
        // Populate form
        document.getElementById('fullName').value = currentUser.full_name || '';
        document.getElementById('bio').value = currentUser.bio || '';
        
        // Update profile picture preview
        if (currentUser.profile_picture) {
            document.getElementById('currentProfilePicture').src = currentUser.profile_picture;
        }
    } catch (err) {
        console.error('Error loading profile:', err);
        window.location.href = '/login';
    }
});

// Handle profile update
document.getElementById('editProfileForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const fullName = document.getElementById('fullName').value.trim();
    const bio = document.getElementById('bio').value.trim();
    const errorDiv = document.getElementById('error');
    const successDiv = document.getElementById('success');
    
    // Clear messages
    errorDiv.textContent = '';
    errorDiv.classList.remove('show');
    successDiv.textContent = '';
    successDiv.classList.remove('show');
    
    try {
        const response = await fetch('/api/profile/me', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ fullName, bio })
        });
        
        if (response.ok) {
            successDiv.textContent = 'Profile updated successfully!';
            successDiv.classList.add('show');
            
            // Update current user data
            currentUser = await response.json();
        } else {
            const data = await response.json();
            errorDiv.textContent = data.error || 'Failed to update profile';
            errorDiv.classList.add('show');
        }
    } catch (err) {
        errorDiv.textContent = 'An error occurred. Please try again.';
        errorDiv.classList.add('show');
    }
});

// Handle profile picture upload
document.getElementById('pictureForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const fileInput = document.getElementById('profilePicture');
    const errorDiv = document.getElementById('error');
    const successDiv = document.getElementById('success');
    
    // Clear messages
    errorDiv.textContent = '';
    errorDiv.classList.remove('show');
    successDiv.textContent = '';
    successDiv.classList.remove('show');
    
    if (!fileInput.files || !fileInput.files[0]) {
        errorDiv.textContent = 'Please select a file';
        errorDiv.classList.add('show');
        return;
    }
    
    const formData = new FormData();
    formData.append('profilePicture', fileInput.files[0]);
    
    try {
        const response = await fetch('/api/profile/me/picture', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            successDiv.textContent = 'Profile picture updated successfully!';
            successDiv.classList.add('show');
            
            // Update preview
            document.getElementById('currentProfilePicture').src = data.profilePicture;
            
            // Clear file input
            fileInput.value = '';
        } else {
            errorDiv.textContent = data.error || 'Failed to upload picture';
            errorDiv.classList.add('show');
        }
    } catch (err) {
        errorDiv.textContent = 'An error occurred. Please try again.';
        errorDiv.classList.add('show');
    }
});

// Handle logout
document.getElementById('logoutBtn').addEventListener('click', async (e) => {
    e.preventDefault();
    try {
        await fetch('/api/auth/logout', { method: 'POST' });
        window.location.href = '/';
    } catch (err) {
        console.error('Logout error:', err);
    }
});

// Handle cancel
document.getElementById('cancelBtn').addEventListener('click', (e) => {
    e.preventDefault();
    if (currentUser) {
        window.location.href = `/profile/${currentUser.username}`;
    } else {
        window.location.href = '/';
    }
});
