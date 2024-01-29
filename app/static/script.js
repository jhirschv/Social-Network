document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll(".like-btn").forEach(button => {
        const postId = button.getAttribute('data-post-id');
        button.addEventListener('click', function() {
            like_post(postId);
        });
        updateLikes(postId);
        updateComments(postId);

    });

    document.querySelectorAll(".comment-box-btn").forEach(commentButton => {
        commentButton.addEventListener('click', function() {
            const postId = commentButton.getAttribute('data-post-id');
            document.querySelector('.comment-box-overlay').style.display = 'block';

            const commentForm = document.querySelector('#comment-form');
            commentForm.onsubmit = function(event) {
                createComment(event, postId);
            };
            updateComments(postId);
        });
    });

    const closeBtn = document.querySelector('#closeBtn');
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            document.querySelector('.comment-box-overlay').style.display = 'none';
        });
    }
});

function createComment(event, postId) {
    event.preventDefault();
    const textarea = document.querySelector('#comment-textarea');
    const comment = document.querySelector('#comment-textarea').value;

    fetch(`/create_comment/${postId}`, {
        method: 'POST',
        body: JSON.stringify({
            comment: comment,
            postId: postId
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        textarea.value = '';
        updateComments(postId)
  });
}

function updateComments(postId) {
    const commentSection = document.querySelector(`#post-comments`);
    const commentCountElement = document.querySelector(`#comment-count-${postId}`)

    fetch(`/update_comments/${postId}`)
    .then(response => response.json())
    .then(data => {
        const commentElement = document.querySelector(`#comment-${postId}`);
        commentCountElement.innerText = data.comment_count;

        if (data.commented) {
            commentElement.classList.add('commented');
        } else {
            commentElement.classList.remove('commented');
        }
        console.log(data.comments);

    commentSection.innerHTML = '';
    if (data.comments && Array.isArray(data.comments) && data.comments.length > 0) {
        data.comments.forEach((comment) => {
            const commentDiv = document.createElement('div');
            commentDiv.className = 'comment';
            commentDiv.innerHTML = `<strong>${comment.user__username}</strong>: ${comment.content}`;
            commentSection.appendChild(commentDiv);
        });
    } else {
        commentSection.innerText = 'No comments yet.';
    }
})
.catch(error => console.error('Error:', error));
}


function like_post(postId) {

    fetch('/like_post/', {
        method: 'POST',
        body: JSON.stringify({ post_id: postId })
    })
    .then(response => response.json())
    .then(result => {

    console.log(result);
    updateLikes(postId);
  });

}

function updateLikes(postId) {

    const heartElement = document.querySelector(`#heart-${postId}`);
    const likeCountElement = document.querySelector(`#like-count-${postId}`);
    fetch(`/update_likes/${postId}`)
    .then(response => response.json())
    .then(data => {
        likeCountElement.innerText = data.likes;

        if (data.liked) {
            heartElement.classList.add('liked');
        } else {
            heartElement.classList.remove('liked');
        }
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });
}