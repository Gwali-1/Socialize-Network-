'use strict'




//elements
const likeBtns = document.querySelectorAll(".like-btn");
const token = document.querySelector("meta[name='token'").getAttribute("content");
const followersNumber = document.querySelector(".followers");
const followBtn = document.querySelector("#follow_unfollow");
const profileError = document.querySelector(".profile-error");
const checkFollow = document.querySelector("#checkFollow");
const page_id =Number(document.querySelector(".page_id").value);
const editPost = document.querySelectorAll(".edit-post");
const saveUpdate = document.querySelectorAll(".save-update")
let follow_action;










//functions

const updatePost = function (event){
    event.preventDefault()
    const postDiv = document.querySelector(`#post-${this.dataset.id}-div`);
    const content = document.querySelector(`#post-${this.dataset.id}-update`);
    const updateForm = document.querySelector(`#update-form-${this.dataset.id}`);
    const postcontent = document.querySelector(`.post-content-${this.dataset.id}`);
    
    console.log(postDiv)
    console.log(content)
    console.log(postcontent)
    ///


    fetch("/edit",{
        method:"PUT",
        headers:{"X-CSRFToken": token},
        body:JSON.stringify({
            id:this.dataset.id,
            new_content:content.value
        })
    }).then(response => response.json()).then(result => {
        if( result.error){
            console.log("err")
            updateForm.classList.add("hidden");
            postDiv.classList.remove("hidden");
        }else{
            updateForm.classList.add("hidden");
            postcontent.textContent = result.new_update;
            postDiv.classList.remove("hidden");
        }
      
        
    }).catch(error => console.log(error))
}





const editPostContent = function (event){
    event.preventDefault();

    const postDiv = document.querySelector(`#post-${this.dataset.id}-div`);
    const postcontent = document.querySelector(`.post-content-${this.dataset.id}`);
    const content = document.querySelector(`#post-${this.dataset.id}-update`);
    const updateForm = document.querySelector(`#update-form-${this.dataset.id}`);

    postDiv.classList.add("hidden");
    updateForm.classList.remove("hidden");
    content.value = postcontent.textContent

}






//changingFollowbuttonLook
const followBtnDisplay = function (state){
    console.log(state)
    if(state){
        followBtn.textContent ="Follow";
        followBtn.classList.remove("followed");
        followBtn.classList.add("unfollowed");
    }else{
        followBtn.textContent ="Following";
        followBtn.classList.remove("unfollowed");
        followBtn.classList.add("followed");
    }
}











//follow/unfollow
const followUnfollow = function () {
    fetch("/follows",{
        method: "PUT",
        headers:{"X-CSRFToken": token},
        body: JSON.stringify({
            id:this.dataset.id,
            follow: follow_action,
        })
    }).then(response => response.json().then(result => {
        if("error" in result){
            console.log("mmmm")
            profileError.textContent = result.error
            return
        }
    

        followBtnDisplay(!result.followed);
        followersNumber.textContent = result.current_followers;
        follow_action=!result.followed;
        console.log(follow_action)


    })).catch(error => console.log(error))
}















//like/unlike
 const likeUnlikePost = function (event) {
    event.preventDefault();

    console.log(Boolean(this.dataset.action))
    fetch("/favourite",{
        method: "PUT",
        headers:{"X-CSRFToken":token},
        body:JSON.stringify({
            id : this.dataset.id,
            like: this.dataset.action
        })
    }).then(response => response.json()).then(result => {
        const btn = document.getElementById(`like-${result.post_id}`);
        btn.textContent = result.current_likes

        if(this.innerHTML ==`<i class="bi bi-hand-thumbs-up"></i>`){
            this.innerHTML = `<i class="bi bi-hand-thumbs-up-fill"></i>`
            this.dataset.action = "false"
            console.log(action,result.liked)
        }else{
            console.log(result)
            this.innerHTML =`<i class="bi bi-hand-thumbs-up"></i>`
            this.dataset.action = "true"
        }
        
    }).catch(error => console.log(error))
}

















//driver code


    likeBtns.forEach(btn => {
        console.log("gooooooo")
        btn.onclick =  likeUnlikePost;
    });


    editPost.forEach(btn =>{
        btn.onclick = editPostContent;
    })


    saveUpdate.forEach(btn => {
        btn.onclick = updatePost;
    })

    






if(page_id == 2){

    if(checkFollow){
        follow_action = false;
    }else{
        follow_action = true;
    }
    if (followBtn){
        followBtnDisplay(follow_action);
        followBtn.onclick = followUnfollow;
    }

    

}





