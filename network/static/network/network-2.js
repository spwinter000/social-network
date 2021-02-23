likeButton.forEach((btn) => { 
    btn.addEventListener("click", () => heartClass(btn.dataset.id));
  });


function heartClass(post_id){
fetch(`/posts/${post_id}`//, {
//   method: 'POST',
//   body: JSON.stringify({
//     post_id: post_id,
//     // likes: post_id.likes
//   })
// }
)
.then(response => response.json())
.then(post => {
console.log(post)
const username = document.getElementById('username').innerHTML;
const likeButton = document.querySelector(`[data-id='${post_id}']`)
  if (post.likes.includes(username)){
    console.log("current user has liked this post")
    likeButton.setAttribute("class", "far fa-heart");
  }
  else{
    console.log("current user has not liked this post")
    likeButton.setAttribute("class", "fas fa-heart");
  }
})
}


function saveEdit(post_id){
  // let editedContent = document.getElementById(`edit-box-${post_id}`).value;
  fetch(`/edit_post/${post_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      post_id: post_id//,
      // content: editedContent
    })
  }
  )
  // .then(response => response.json())
  .then( 
    result => {
      console.log('save edit function clicked')
      // console.log(result)
      // for (post of result){
      //   console.log(post)
      // }

      if(result.status === 200){

        const editedContent = document.getElementById(`edit-box-${post_id}`).value;
        document.getElementById(`content-${post_id}`).innerHTML = editedContent;

        const content = document.getElementById(`content-${post_id}`);
        const editBox = document.getElementById(`edit-box-${post_id}`);

        const saveButton = document.getElementById(`save-button-${post_id}`);
        const editButton = document.querySelector(`[data-id='edit-${post_id}']`);
        
        // content.name = 'updated-content';
        content.style.display = 'block';
        editButton.style.display = 'block';

        console.log(editBox.name)
        console.log(editBox.value);
        console.log(content.innerHTML);
        
        saveButton.remove();
        editBox.remove();
      
      }
    })
    .catch(error => {
      console.log('Error:', error);
    });
    return false;
}


function saveEdit(post_id){
  // let editedContent = document.getElementById(`edit-box-${post_id}`).value;

  const editedContent = document.getElementById(`edit-box-${post_id}`).value;
  document.getElementById(`content-${post_id}`).innerHTML = editedContent;

  const content = document.getElementById(`content-${post_id}`);
  const editBox = document.getElementById(`edit-box-${post_id}`);

  const saveButton = document.getElementById(`save-button-${post_id}`);
  const editButton = document.querySelector(`[data-id='edit-${post_id}']`);
  
  // content.name = 'updated-content';
  content.style.display = 'block';
  editButton.style.display = 'block';

  console.log(editBox.name)
  console.log(editBox.value);
  console.log(content.innerHTML);
  
  saveButton.remove();
  editBox.remove();

  if (post_id){
  fetch(`/edit_post/${post_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      post_id: post_id,
      content: content.innerHTML
    })
  }
  )
  .then(response => response.json())
  .then( 
    result => {
      console.log('save edit function clicked')
      // console.log(result)
      // for (post of result){
        result.content = content.innerHTML
        console.log(result)
      // }
      
      // }
    })
    .catch(error => {
      console.log('Error:', error);
    });
    return false;
  }
}
