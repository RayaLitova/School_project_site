document.body.style.backgroundColor = localStorage.page;
document.getElementById('navbar').style.backgroundColor = localStorage.nav_color;
document.getElementById('results').style.color = localStorage.txt;
document.getElementById('field').style.color = localStorage.txt;
let txt = document.getElementsByClassName("h1");
for (x <= txt.length; x = 0; x += 1) {
    txt[x].style.color = localStorage.txt;
};