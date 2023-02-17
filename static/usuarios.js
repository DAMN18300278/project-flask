inicio = document.getElementById("inicioMenu");
ojos = document.getElementById("ojosMenu");
labios = document.getElementById("labiosMenu");
piel = document.getElementById("pielMenu");
skincare = document.getElementById("skincareMenu");
accesorios = document.getElementById("accesoriosMenu");
selected = document.getElementsByClassName("horizontal-menu-hover")

document.addEventListener("DOMContentLoaded", function ojosBorderLeft() {
    horizontalMenuChange(1);
});

function horizontalMenuChange(element) {
    selected[0].classList.add("horizontal-menu-unset");
    selected[0].classList.remove("horizontal-menu-hover");
    switch (element) {
        case 1:
            inicio.classList.add("horizontal-menu-hover");
            break;
        case 2:
            ojos.classList.add("horizontal-menu-hover");
            break;
        case 3:
            labios.classList.add("horizontal-menu-hover");
            break;
        case 4:
            piel.classList.add("horizontal-menu-hover");
            break;
        case 5:
            skincare.classList.add("horizontal-menu-hover");
            break;
        case 6:
            accesorios.classList.add("horizontal-menu-hover");
            break;
    }
}