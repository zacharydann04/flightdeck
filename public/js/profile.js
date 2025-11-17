document.addEventListener('DOMContentLoaded', async () => {
    // Get username from URL
    const pathParts = window.location.pathname.split('/');
    const username = pathParts[pathParts.length - 1];
    
    try {
        // Fetch profile data
        const response = await fetch(`/api/profile/${username}`);
        
        if (!response.ok) {
            if (response.status === 404) {
                document.getElementById('username').textContent = 'User not found';
                return;
            }
            throw new Error('Failed to fetch profile');
        }
        
        const profile = await response.json();
        
        // Update profile information
        document.getElementById('username').textContent = profile.username;
        document.getElementById('fullName').textContent = profile.full_name || '';
        document.getElementById('bio').textContent = profile.bio || '';
        
        // Update profile picture
        if (profile.profile_picture) {
            document.getElementById('profilePicture').src = profile.profile_picture;
        }
        
        // Format member since date
        const createdDate = new Date(profile.created_at);
        document.getElementById('memberSince').textContent = createdDate.toLocaleDateString('en-US', {
            month: 'long',
            year: 'numeric'
        });
        
        // Check if viewing own profile
        const currentUserResponse = await fetch('/api/profile/me');
        if (currentUserResponse.ok) {
            const currentUser = await currentUserResponse.json();
            if (currentUser.id === profile.id) {
                document.getElementById('editButton').style.display = 'block';
            }
        }
    } catch (err) {
        console.error('Error loading profile:', err);
        document.getElementById('username').textContent = 'Error loading profile';
    }
});
