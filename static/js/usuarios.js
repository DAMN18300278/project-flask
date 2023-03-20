document.addEventListener("DOMContentLoaded", () => {
    var url = $(location).attr('href')
    if(!url.includes('formulario')){
        horizontalMenuChange(1);
    }
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
            var positionAt = document.getElementById("inicioDiv");
            document.getElementById("container-div-index").scrollTo({
                left: positionAt.offsetLeft,
                behavior: "smooth"
            })
            inicio.classList.add("horizontal-menu-hover");
            break;
        case 2:
            var positionAt = document.getElementById("ojosDiv");
            document.getElementById("container-div-index").scrollTo({
                left: positionAt.offsetLeft,
                behavior: "smooth"
            })
            ojos.classList.add("horizontal-menu-hover");
            break;
        case 3:
            var positionAt = document.getElementById("inicioDiv");
            document.getElementById("container-div-index").scrollTo({
                left: positionAt.offsetLeft,
                behavior: "smooth"
            })
            labios.classList.add("horizontal-menu-hover");
            break;
        case 4:
            var positionAt = document.getElementById("inicioDiv");
            document.getElementById("container-div-index").scrollTo({
                left: positionAt.offsetLeft,
                behavior: "smooth"
            })
            piel.classList.add("horizontal-menu-hover");
            break;
        case 5:
            var positionAt = document.getElementById("inicioDiv");
            document.getElementById("container-div-index").scrollTo({
                left: positionAt.offsetLeft,
                behavior: "smooth"
            })
            skincare.classList.add("horizontal-menu-hover");
            break;
        case 6:
            var positionAt = document.getElementById("inicioDiv");
            document.getElementById("container-div-index").scrollTo({
                left: positionAt.offsetLeft,
                behavior: "smooth"
            })
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

$(document).ready(function() {
    // Obtener el input de búsqueda y el menú desplegable
    var $search = $(".dropdown-menu input");
    var $dropdownMenu = $(".dropdown-menu");
  
    // Filtrar los elementos del menú desplegable al escribir en el input de búsqueda
    $search.keyup(function() {
        var filter = $(this).val().toLowerCase();
        var $items = $dropdownMenu.find("a");
        $items.each(function() {
            var text = $(this).text().toLowerCase();
            var match = text.indexOf(filter) > -1;
            $(this).toggle(match);
        });
    });
});

$(document).ready(function ($) {
    $('#tabs').tab();
});