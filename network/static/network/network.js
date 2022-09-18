'use strict'



//elements
const likeBtns = document.querySelectorAll(".like-btn");
const token = document.querySelector("meta[name='token'").getAttribute("content");
const followersNumber = document.querySelector(".followers");
const followBtn = document.querySelector("#follow_unfollow");
const profileError = document.querySelector(".profile-error");
const checkFollow = document.querySelector("#checkFollow");


let follow_action;

let action = true




if(checkFollow){
    follow_action = false;
}else{
    follow_action = true;
}

console.log("action",follow_action)



//functions

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



followBtnDisplay(follow_action);


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
        
        

        //change follow button state
        // if(result.followed){
        //     followBtn.textContent ="Following";
        //     followBtn.classList.remove("unfollowed");
        //     followBtn.classList.add("followed");
        // }else{
        //     followBtn.textContent ="Follow";
        //     followBtn.classList.remove("followed");
        //     followBtn.classList.add("unfollowed");
        // }

        followBtnDisplay(!result.followed);
        followersNumber.textContent = result.current_followers;
        follow_action=!result.followed;
        console.log(follow_action)

        // if(followBtn.classList.contains("unfollowed")){
            
        // }else{
        //     console.log(followBtn)
           
        // }
       


    }))
}





const likeUnlikePost = function (e) {
    e.preventDefault();
    fetch("/favourite",{
        method: "PUT",
        headers:{"X-CSRFToken":token},
        body:JSON.stringify({
            id : this.dataset.id,
            like: action
        })
    }).then(response => response.json()).then(result => {
        const btn = document.getElementById(`like-${result.post_id}`);
        btn.textContent = result.current_likes

        if(this.innerHTML ==`<i class="bi bi-hand-thumbs-up"></i>`){
            this.innerHTML = `<i class="bi bi-hand-thumbs-up-fill"></i>`
            action=!result.liked
            console.log(action,result.liked)
        }else{
            this.innerHTML =`<i class="bi bi-hand-thumbs-up"></i>`
            action=!result.liked
            console.log(action,result.liked)
        }
        
    }).catch(error => console.log(error))
}








likeBtns.forEach(btn => {
    btn.onclick = likeUnlikePost
});


followBtn.onclick = followUnfollow;
