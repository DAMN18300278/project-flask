document.addEventListener("DOMContentLoaded", () => {
    var url = $(location).attr('href')
    if(!url.includes('formulario')){
        horizontalMenuChange(1);
    }
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
    
    document.getElementById("body").style.display = "block"; 
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

    $('#tabsMenu').tab();

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

        var textProduct = boton.data('producto');
        var sinComillas = textProduct.replace('\n\n', " ");
        var sinTabs = sinComillas.replace(/'/g, "\"");
        
        productJson = JSON.parse(sinTabs); 
        
        var productoId = productJson['Id'];
        var cantidadImgs = productJson['Imagenes'];
        var nombre = productJson['Nombre'];
        var descripcion = productJson['Descripcion'];
        var tipoPiel = productJson['Tipo de piel'];
        var colores = productJson['Colores'];
        var marca = productJson['Marca'];
        var tipo = productJson['Tipo'];
        var precio = productJson['Precio u.'];
        
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

        var boton = $(this)
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

const animateCSS = (element, animation, prefix = 'animate__') =>
// We create a Promise and return it
new Promise((resolve, reject) => {
    const animationName = `${prefix}${animation}`;
    const node = document.getElementById(element);

    node.classList.add(`${prefix}animated`, animationName);

    // When the animation ends, we clean the classes and resolve the Promise
    function handleAnimationEnd(event) {
        event.stopPropagation();
        node.classList.remove(`${prefix}animated`, animationName);
        resolve('Animation ended');
        console.log('ya');
    }

    node.addEventListener('animationend', handleAnimationEnd, {once: true});
});

// let i = 0;
// setInterval(function(){
//     i++;
//     document.getElementById('cantidadCarrito').textContent = i;
//     animateCSS('carrito', 'rotateInDownRight');
// }, 2000)
