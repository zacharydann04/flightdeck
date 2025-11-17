// Like button functionality
document.addEventListener('DOMContentLoaded', function() {
    // Handle like buttons
    const likeButtons = document.querySelectorAll('.like-btn');
    likeButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const postId = this.dataset.postId;
            
            try {
                const response = await fetch(`/post/${postId}/like`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Update like count
                    const likeCount = this.querySelector('.like-count');
                    likeCount.textContent = data.like_count;
                    
                    // Toggle liked class
                    if (data.liked) {
                        this.classList.add('liked');
                    } else {
                        this.classList.remove('liked');
                    }
                }
            } catch (error) {
                console.error('Error liking post:', error);
            }
        });
    });
    
    // Handle comment form
    const commentForms = document.querySelectorAll('.comment-form');
    commentForms.forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const postId = this.dataset.postId;
            const textarea = this.querySelector('textarea[name="content"]');
            const content = textarea.value;
            
            if (!content.trim()) {
                return;
            }
            
            try {
                const formData = new FormData();
                formData.append('content', content);
                
                const response = await fetch(`/post/${postId}/comment`, {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Add new comment to the list
                    const commentsList = document.querySelector('.comments-list');
                    const commentHTML = `
                        <div class="comment">
                            <div class="comment-header">
                                <a href="/profile/${data.comment.author}" class="comment-author">
                                    @${data.comment.author}
                                </a>
                                <span class="comment-date">${data.comment.created_at}</span>
                            </div>
                            <p class="comment-content">${data.comment.content}</p>
                        </div>
                    `;
                    commentsList.insertAdjacentHTML('afterbegin', commentHTML);
                    
                    // Clear the textarea
                    textarea.value = '';
                } else {
                    alert('Error adding comment: ' + data.error);
                }
            } catch (error) {
                console.error('Error adding comment:', error);
                alert('Error adding comment');
            }
        });
    });
});
