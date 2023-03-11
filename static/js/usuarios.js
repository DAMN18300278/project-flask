document.addEventListener("DOMContentLoaded", () => {
    horizontalMenuChange(1);
    document.getElementById("body").style.display = "block";
});

function horizontalMenuChange(element) {
    inicio = document.getElementById("inicioMenu");
    ojos = document.getElementById("ojosMenu");
    labios = document.getElementById("labiosMenu");
    piel = document.getElementById("pielMenu");
    skincare = document.getElementById("skincareMenu");
    accesorios = document.getElementById("accesoriosMenu");
    selected = document.getElementsByClassName("horizontal-menu-hover");
    

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

function snapContainerTranslateLeft(e) {
    switch (e) {
        case 1:
            snapProductosPopulares = document.getElementById("snapProductosPopulares");
            snapProductosPopulares.scrollBy({
                top: 0,
                left: -150,
                behavior: 'smooth'
            })
            break;
        case 2:
            snapBestSeller = document.getElementById("snapBestSeller");
            snapBestSeller.scrollBy({
                top: 0,
                left: -150,
                behavior: 'smooth'
            })
            break;
        case 3:
            snapSelectedForUser = document.getElementById("snapSelectedForUser");
            snapSelectedForUser.scrollBy({
                top: 0,
                left: -150,
                behavior: 'smooth'
            })
            break;
        case 4:
            snapSelectedForUser = document.getElementById("snapInfoProductos");
            snapSelectedForUser.scrollBy({
                top: 0,
                left: -150,
                behavior: 'smooth'
            })
            break;
    }
}

function snapContainerTranslateRight(e) {
    switch (e) {
        case 1:
            snapProductosPopulares = document.getElementById("snapProductosPopulares");
            snapProductosPopulares.scrollBy({
                top: 0,
                left: +150,
                behavior: 'smooth'
            })
            break;
        case 2:
            snapBestSeller = document.getElementById("snapBestSeller");
            snapBestSeller.scrollBy({
                top: 0,
                left: +150,
                behavior: 'smooth'
            })
            break;
        case 3:
            snapSelectedForUser = document.getElementById("snapSelectedForUser");
            snapSelectedForUser.scrollBy({
                top: 0,
                left: +150,
                behavior: 'smooth'
            })
            break;
        case 4:
            snapSelectedForUser = document.getElementById("snapInfoProductos");
            snapSelectedForUser.scrollBy({
                top: 0,
                left: +150,
                behavior: 'smooth'
            })
            break;
    }

}
