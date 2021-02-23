// change following button to 'unfollow' on mouseover
document.addEventListener('DOMContentLoaded', function() {
    let button = document.getElementById('follow');
    if(button.value === "Follow"){
      console.log('request.user is not following this user');
      button.value === "Follow";
    }
    else {
        button.addEventListener('mouseover', function(event){
            event.target.value = 'Unfollow';
            event.target.className = 'btn btn-danger';
        })
        button.addEventListener('mouseout', function(event){
            event.target.value = 'Following';
            event.target.className = 'btn btn-primary';
    });
    console.log('request.user is following this user');
    }
  });

// assign full-heart class to like icon if current user has liked a post
document.addEventListener('DOMContentLoaded', function() {
  fetch(`/posts`)
  .then(response => response.json())
  .then(posts => {
    // console.log(posts)
    if(posts.length === 0){
      console.log('no posts yet');
    } else {
      for (post of posts){
        // posts.forEach(post => {
          // console.log(post);
          const username = document.getElementById('username').innerHTML;
          const likeButton = document.querySelector(`[data-id='${post.id}']`)
          // if(posts.includes(post)){
            if(likeButton === null){
              continue;
            }
            else {
              if (post.likes.includes(username)){
            // console.log("current user has liked this post")
            likeButton.setAttribute("class", "fas fa-heart");
          }
          else{
            // console.log("current user has not liked this post")
            likeButton.setAttribute("class", "far fa-heart");
          }
        }
      }
    }
  })
})

// add event listeners for edit and like buttons
document.addEventListener('DOMContentLoaded', function() {
  const editButton = document.querySelectorAll('.edit-button');

  editButton.forEach((btn) => { 
      btn.addEventListener("click", () => edit(btn.id));
    });

  const likeButton = document.querySelectorAll('#like-button');

  likeButton.forEach((btn) => { 
      btn.addEventListener("click", () => like(btn.dataset.id));
    });
});

// edit a post
function edit(post_id){
  const editButton = document.querySelector(`[data-id='edit-${post_id}']`)
  editButton.style.display = 'none';

  const postTop = document.getElementById(`post-top-${post_id}`)

  // hide orginal content
  const pic = document.getElementById(`post-pic-${post_id}`);
  pic.style.display = 'none';

  const name = document.getElementById(`name-${post_id}`);
  name.style.display = 'none';

  const content = document.getElementById(`content-${post_id}`);
  content.style.display = 'none';

  const timestamp = document.querySelector(`[data-id='timestamp-${post_id}']`)
  timestamp.style.display = 'none';

  // create textarea for edits
  const editBox = document.createElement('textarea');
  editBox.id = `edit-box-${post_id}`;
  editBox.className = 'edit-box';
  editBox.name = 'updated-content';
  editBox.value = content.innerHTML;

  // create save button
  const saveButton = document.createElement('input');
  saveButton.id = `save-button-${post_id}`;
  saveButton.className = "save-button";
  saveButton.type = 'Submit';
  saveButton.dataset.id = `save-${post_id}`;
  saveButton.value = 'Save';

  postTop.append(editBox, saveButton);
  
  saveButton.addEventListener("click", () => saveEdit(post_id));
}

// get cookie for saveEdit function
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

// save the edit thats made...
function saveEdit(post_id){

  // set contents of editBox equal to content's innerHTML, then hide and show appropriate elements
  const editedContent = document.getElementById(`edit-box-${post_id}`).value;
  document.getElementById(`content-${post_id}`).innerHTML = editedContent;

  const content = document.getElementById(`content-${post_id}`);
  const editBox = document.getElementById(`edit-box-${post_id}`);
  const timestamp = document.querySelector(`[data-id='timestamp-${post_id}']`)
  const pic = document.getElementById(`post-pic-${post_id}`);
  const name = document.getElementById(`name-${post_id}`);
  
  const saveButton = document.getElementById(`save-button-${post_id}`);
  const editButton = document.querySelector(`[data-id='edit-${post_id}']`);
  
  
  // make sure content doesnt have awkward spacing after save
  content.style.display = 'block';
  content.style.marginTop = 0;
  
  pic.style.display = 'block';
  name.style.display = 'inline';
  editButton.style.display = 'block';
  timestamp.style.display = 'inline';
  
  saveButton.remove();
  editBox.remove();

  if (post_id){
  fetch(`/edit_post/${post_id}`, {
    credentials: 'include',
    method: 'POST',
    mode: 'same-origin',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken') 
    },
    // method: 'PUT',
    body: JSON.stringify({
      post_id: post_id,
      content: content.innerHTML
    })
  }
  )
  .then(response => response.json())
  .then( 
    result => {
        result.content = content.innerHTML
    })
    .catch(error => {
      console.log('Error:', error);
    });
    return false;
  }
}

// increase/decrease likes
function like(post_id){
  fetch(`/like/${post_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      post_id: post_id
    })
  }
  )
  .then(
    result => {
    if(result.status === 200){
      let likes = parseInt(document.getElementById(`likes-count-${post_id}`).innerHTML);

      const likeButton = document.querySelector(`[data-id='${post_id}']`)

      if (likeButton.className === "far fa-heart"){
        likeButton.setAttribute("class", "fas fa-heart");
        likes++;
        document.getElementById(`likes-count-${post_id}`).innerHTML = likes;
      } else {
        likeButton.setAttribute("class", "far fa-heart");
        likes--;
        document.getElementById(`likes-count-${post_id}`).innerHTML = likes;
      }
    }
  }
  )
  .catch(error => {
    console.log('Error:', error);
  });
}