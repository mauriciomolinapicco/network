document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.edit-button').forEach(button => {
        button.addEventListener('click', () => {
            //postElement is the div containing a single post
            const singlePost = button.closest('.singlePost');
            singlePost.querySelector('.post-content').style.display = 'none';
            singlePost.querySelector('.edit-button').style.display = 'none';
            singlePost.querySelector('.edit-post').style.display = 'block';
        })
    });

    document.querySelectorAll('.save-button').forEach(button => {
        button.addEventListener('click', () => {
            const singlePost = button.closest('.singlePost');
            const content = singlePost.querySelector('.edit-textarea').value;
            const postId = singlePost.dataset.postId;

            fetch(`/editpost/${postId}`, {
                method: 'PUT',
                body: JSON.stringify({
                    content: content
                })
              })
            .then(response => {
                if (response.ok) {
                    return response.text();
                } throw new Error('Something went wrong.');
            })
           .then(data => {
                singlePost.querySelector('.post-content').textContent = content;
                singlePost.querySelector('.post-content').style.display = 'block';
                singlePost.querySelector('.edit-button').style.display = 'inline';
                singlePost.querySelector('.edit-post').style.display = 'none';
           })
  
        })
    })


    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', () => {
            const singlePost = button.closest('.singlePost');
            const postId = singlePost.dataset.postId;
            const like = button.dataset.like;
            let booleanValue = true;
            if (like === 'true') {
                booleanValue = true;
            } else {
                booleanValue = false;
            }
            fetch("/likepost", {
                method: 'POST',
                body: JSON.stringify({
                    like: booleanValue,
                    post_id: postId
                })
            })
            .then(function(response) {                      
                if(response.ok)
                {
                  return response.text();         
                }
                throw new Error('Something went wrong.');
            })  
            .then(data => {
                const likeCount = parseInt(button.dataset.count);
                const counter = singlePost.querySelector('.like-count');
                if (like === 'true') {
                    button.dataset.like = 'false';
                    button.classList.remove('btn-primary');
                    button.classList.add('btn-danger');
                    button.textContent = 'Unlike';
                    counter.textContent = '❤️'+String(likeCount+1);
                } else {
                    button.dataset.like = 'true';
                    button.classList.remove('btn-danger');
                    button.classList.add('btn-primary');
                    button.textContent = 'Like';
                    counter.textContent = '🤍'+ String(likeCount-1);
                }
                
    
            })

            .catch(function(error) {
              console.log('Request failed', error);
            });
        })
    })
})


function edit() {
    document.querySelector('#oldButton').style.display = 'none';
    let textarea = document.createElement('textarea');
    let editDiv = document.querySelector('#editPost');
    editDiv.appendChild(textarea);
    editDiv.style.display = 'block';
}