var settingMenu= document.querySelector(".settings-menu");
var darrkBtn= document.getElementById("dark-btn")
const open = document.getElementById('open');
const modal_container = document.getElementById('modal_container');
const close = document.getElementById('close');

function settingMenuToggle(){
    settingMenu.classList.toggle("setting-menu-height");


}
darrkBtn.onclick=function(){
    darrkBtn.classList.toggle("dark-btn-on");
    document.body.classList.toggle("dark-theme")
}


function settingPerfilToggle(){
  settingMenu.classList.toggle("setting-profile");


}

open.addEventListener('click', () => {
  modal_container.classList.add('show');  
});

close.addEventListener('click', () => {
  modal_container.classList.remove('show');
});





