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

function _calculateScrollbarHeight() {
    document.documentElement.style.setProperty(
      "--scrollbar-height",
      window.innerWidth - document.documentElement.clientWidth + "px"
    );
  }
  
  // recalculate on dom load
  document.addEventListener("DOMContentLoaded", _calculateScrollbarHeight, false);
  // recalculate on load (assets loaded as well)
  window.addEventListener("load", _calculateScrollbarHeight);
  // recalculate on resize
  window.addEventListener("resize", _calculateScrollbarHeight, false);