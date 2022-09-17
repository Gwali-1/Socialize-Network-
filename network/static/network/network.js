'use strict'



//elements
const likeBtns = document.querySelectorAll(".like-btn");
const token = document.querySelector("meta[name='token'").getAttribute("content")


console.log(token)
// console.log(token.getAttribute("content"))

console.log(document.querySelector(".token").value)


let action = true



//functions

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
        
    })
}



likeBtns.forEach(btn => {
    btn.onclick = likeUnlikePost
});


