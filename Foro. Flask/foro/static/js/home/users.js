const imgsContainer = Array.from(document.querySelectorAll(".users_container_list img"))
const documentFragment = document.createDocumentFragment()

const users = JSON.parse(document.querySelector(".users_container").dataset.users);

const mediaQuery = window.matchMedia("(min-width: 1024px)")

const handleHoverCard = (e) => {
    const idImg = e.target.alt

    const user = users.find(user => user.nick === idImg)

    const userContainer = document.querySelector(`.${user.nick}_container`)

    if (!document.querySelector(".card-container")){
        userContainer.insertBefore(handleRenderHtml(user.img, user.nick), userContainer.firstChild)
    }
    
   document.querySelector(".card-container").addEventListener("mouseleave", handleRemoveHoverCard)
}

const handleHoverCardMobile = (e) => {
    const idImg = e.target.alt

    const user = users.find(user => user.nick === idImg)

    const userContainer = document.querySelector(`.${user.nick}_container`)

    if (!document.querySelector(".card-container")){
        userContainer.insertBefore(handleRenderHtml(user.img, user.nick), userContainer.firstChild)
    }

    document.querySelector(".card-container").addEventListener("click", handleRemoveHoverCard);

}

const handleRemoveHoverCard = (e) => {

    document.querySelector(`.card-container`).remove()

}

imgsContainer.map(img => {
    if (mediaQuery.matches){
        img.addEventListener("mouseover", handleHoverCard);
    } else {
        img.addEventListener("click", handleHoverCardMobile);
    }
})

const handleRenderHtml = (img, nick) => {

    const div = document.createElement("div")

    const html = `<img class="" src="/static/profilephotos/${img}" alt="${nick}">
                    <a href="/profile/${nick}"><h2>${nick}</h2></a>`

    div.innerHTML = html;

    div.setAttribute("class", `card-container`)

    return div

}