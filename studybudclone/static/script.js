const drop_btn = document.querySelector(".drop-btn");
const dropdown = document.querySelector(".dropdown");
// var room_participants_body = document.querySelector(".room .activity.box-layout .room__body");

drop_btn.onclick = (() => {
    dropdown.classList.toggle("show");
});

// var y = room_participants_body.getBoundingClientRect().top;
// room_participants_body.style.height = document.documentElement.clientHeight - y - 13 + 'px';