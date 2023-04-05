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
            var temp = document.getElementById("container-div-index");
            var rect = positionAt.getBoundingClientRect();
            var left = rect.left;
            temp.scrollTo({
                left: positionAt.offsetLeft,
                behavior: "smooth"
            })
            inicio.classList.add("horizontal-menu-hover");
            break;
        case 2:
            var positionAt = document.getElementById("pielDiv");
            var temp = document.getElementById("container-div-index");
            var rect = positionAt.getBoundingClientRect();
            var left = rect.left;
            temp.scrollTo({
                left: positionAt.offsetLeft,
                behavior: "smooth"
            })
            ojos.classList.add("horizontal-menu-hover");
            break;
        case 3:
            var positionAt = document.getElementById("labiosDiv");
            var temp = document.getElementById("container-div-index");
            var rect = positionAt.getBoundingClientRect();
            var left = rect.left;
            temp.scrollTo({
                left: positionAt.offsetLeft,
                behavior: "smooth"
            })
            labios.classList.add("horizontal-menu-hover");
            break;
        case 4:
            var positionAt = document.getElementById("inicioDiv");
            var temp = document.getElementById("container-div-index");
            var rect = positionAt.getBoundingClientRect();
            var left = rect.left;
            temp.scrollTo({
                left: left,
                behavior: "smooth"
            })
            piel.classList.add("horizontal-menu-hover");
            break;
        case 5:
            var positionAt = document.getElementById("inicioDiv");
            var temp = document.getElementById("container-div-index");
            var rect = positionAt.getBoundingClientRect();
            var left = rect.left;
            temp.scrollTo({
                left: left,
                behavior: "smooth"
            })
            skincare.classList.add("horizontal-menu-hover");
            break;
        case 6:
            var positionAt = document.getElementById("inicioDiv");
            var temp = document.getElementById("container-div-index");
            var rect = positionAt.getBoundingClientRect();
            var left = rect.left;
            temp.scrollTo({
                left: left,
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
            snapInfoProductos = document.getElementById("snapInfoProductos");
            snapInfoProductos.scrollBy({
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
            snapInfoProductos = document.getElementById("snapInfoProductos");
            snapInfoProductos.scrollBy({
                top: 0,
                left: +150,
                behavior: 'smooth'
            })
            break;
    }
}

$(document).ready(function ($) {
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

    $('#tabs').tab();

    $('#infoProducto').on('show.bs.modal', function(event){
        var boton = $(event.relatedTarget);
        var modal = $(this);
        var contentImgs = '';
        var contentColores = '';
        var tiposPiel = {
            1: 'Normal',
            2: 'Seca',
            3: 'Grasa',
            4: 'Mixta',
            5: 'Acné',
            6: 'Sensible'
        };
        
        var productoId = boton.data('producto-id');
        var cantidadImgs = boton.data('cantidad-imgs');
        var nombre = boton.data('nombre');
        var descripcion = boton.data('descripcion');
        var tipoPiel = boton.data('tipo-piel');
        var stringColores = boton.data('colores');
        var marca = boton.data('marca');
        var tipo = boton.data('tipo');
        var precio = boton.data('precio');

        var colores = JSON.parse(stringColores.replace(/'/g, "\""));
        
        for (var i = 0; i < cantidadImgs; i++) {
            var imgModal = 'static/src/img' + productoId + '_' + (i+1) + '.jpg';
            contentImgs += '<div class="snap-section"><img class="imgInfo" src="' + imgModal + '"></div>';
        }
        
        $('#snapInfoProductos').animate({scrollLeft: 0}, 500);
        modal.find('#snapInfoProductos').html(contentImgs);
        modal.find('#idInfoProductos').text("#" + productoId.toString().padStart(5, "0"));
        modal.find('#nombreInfoProductos').text(nombre);
        modal.find('#descInfoProductos').text(descripcion);
        if(tipoPiel == '1'){
            modal.find('#tipoPielInfoProductos').text("No afecta a la piel");
        }else{
            modal.find('#tipoPielInfoProductos').text("Piel que afecta: " + tiposPiel[tipoPiel]);
        }
        for (var key in colores){
            contentColores += "<div class='colores-info col-3 m-2' data-color='" + colores[key]['Nombre'] + "'style='background-color: #" + colores[key]['Hex'] + ";'></div>"
        }
        modal.find('#hexColorInfoProductos').html(contentColores);
        modal.find('#marcaInfoProductos').text('Marca: ' + marca.toLowerCase().replace(/\b\w/g, function(l){ return l.toUpperCase(); }));
        modal.find('#tipoInfoProductos').text('Tipo: ' + tipo);
        modal.find('#precioInfoProductos').text('$' + precio);
    });

    $('#infoProducto').on('hidden.bs.modal', function(){
        var modal = $(this);
        modal.find('#cantidad').val(1);
        modal.find('#nombreColorInfoProductos').text('Color');
    });

    $('#btn-minus').click(function() {
        var input = $('#cantidad');
        var value = parseInt(input.val());
        if (value > 1) {
            input.val(value - 1);
        }
    });

    $('#btn-plus').click(function() {
        var input = $('#cantidad');
        var value = parseInt(input.val());
        input.val(value + 1);
    });

});

$(document).on('click', '.colores-info', function(event){
    var input = $(event.target);
    var nombreColor = input.data('color');
    var output = $('#nombreColorInfoProductos');

    $('.colores-info').removeClass('colores-info-selected');
    input.addClass('colores-info-selected');
    
    output.text(nombreColor)
});

