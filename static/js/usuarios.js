document.addEventListener("DOMContentLoaded", () => {
    var url = $(location).attr('href')
    if(!url.includes('formulario')){
        horizontalMenuChange(1);
    }
});

function ircarrito(){
    window.location.href = "/usuarios/ordencarrito/"+idUsuario;
}

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
            piel.classList.add("horizontal-menu-hover");
            break;
        case 3:
            labios.classList.add("horizontal-menu-hover");
            break;
        case 4:
            ojos.classList.add("horizontal-menu-hover");
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
    
    // Filtrar los elementos del menú desplegable al escribir en el input de búsqueda
    var originalItemsOjos = $("#dropdownSearchOjosList").find("#itemOjos[data-nombre]").clone();
    var originalItemsLabios = $("#dropdownSearchLabiosList").find("#itemLabios[data-nombre]").clone();
    var originalItemsPiel = $("#dropdownSearchPielList").find("#itemPiel[data-nombre]").clone();
    var originalItemsSkin = $("#dropdownSearchSkinList").find("#itemSkin[data-nombre]").clone();
    var originalItemsAccesorios = $("#dropdownSearchAccesoriosList").find("#itemAccesorios[data-nombre]").clone();

    $("#searchMenuLabios").keyup(function() {
        var filter = $(this).val().toLowerCase();
        var items = $("#dropdownSearchLabiosList").find("#itemLabios[data-nombre], #itemLabios[data-id]");
        items.each(function() {
            var productName = $(this).text().toLowerCase();
            var nombre = $(this).data("nombre").toLowerCase();
            var id = $(this).data("id");
            var match = productName.indexOf(filter) > -1 || nombre.indexOf(filter) > -1 || id.toString().indexOf(filter) > -1;
            $(this).toggle(match);
        });
    });
    $("#searchMenuOjos").keyup(function() {
        var filter = $(this).val().toLowerCase();
        var items = $("#dropdownSearchOjosList").find("#itemOjos[data-nombre]");
        items.each(function() {
            var productName = $(this).text().toLowerCase();
            var match = productName.indexOf(filter) > -1;
            $(this).toggle(match);
        });
    });
    $("#searchMenuPiel").keyup(function() {
        var filter = $(this).val().toLowerCase();
        var items = $("#dropdownSearchPielList").find("#itemPiel[data-nombre]");
        items.each(function() {
            var productName = $(this).text().toLowerCase();
            var match = productName.indexOf(filter) > -1;
            $(this).toggle(match);
        });
    });
    $("#searchMenuSkin").keyup(function() {
        var filter = $(this).val().toLowerCase();
        var items = $("#dropdownSearchSkinList").find("#itemSkin[data-nombre]");
        items.each(function() {
            var productName = $(this).text().toLowerCase();
            var match = productName.indexOf(filter) > -1;
            $(this).toggle(match);
        });
    });
    $("#searchMenuAccesorios").keyup(function() {
        var filter = $(this).val().toLowerCase();
        var items = $("#dropdownSearchAccesoriosList").find("#itemAccesorios[data-nombre]");
        items.each(function() {
            var productName = $(this).text().toLowerCase();
            var match = productName.indexOf(filter) > -1;
            $(this).toggle(match);
        });
    });

    $('#dropdownSearchLabios').on('hidden.bs.dropdown', function(){
        $('#searchMenuLabios').val("");
        $("#dropdownSearchLabiosList").empty().append(originalItemsLabios.clone());
    });
    $('#dropdownSearchOjos').on('hidden.bs.dropdown', function(){
        $('#searchMenuOjos').val("");
        $("#dropdownSearchOjosList").empty().append(originalItemsOjos.clone());
    });
    $('#dropdownSearchPiel').on('hidden.bs.dropdown', function(){
        $('#searchMenuPiel').val("");
        $("#dropdownSearchPielList").empty().append(originalItemsPiel.clone());
    });
    $('#dropdownSearchSkin').on('hidden.bs.dropdown', function(){
        $('#searchMenuSkin').val("");
        $("#dropdownSearchSkinList").empty().append(originalItemsSkin.clone());
    });
    $('#dropdownSearchAccesorios').on('hidden.bs.dropdown', function(){
        $('#searchMenuAccesorios').val("");
        $("#dropdownSearchAccesoriosList").empty().append(originalItemsAccesorios.clone());
    });

    $('#tabs').tab();

    $('#tabsMenu').tab();
    $('#tabsMenu2').tab();

    var productoId;
    var contentColores;
    var keySeleccionado;
    
    $('#infoProducto').on('show.bs.modal', function(event){
        var boton = $(event.relatedTarget);
        var modal = $(this);
        var contentImgs = '';
        contentColores = '';
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
        
        productoId = productJson['Id'];
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
        modal.find('#idInfoProductos').text("ID: #" + productoId.toString());
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
        modal.find('.colores-info').on('click', function(){
        var colorSeleccionado = $(this).data('color');
        keySeleccionado
        for (var key in colores) {
            if (colores[key]['Nombre'] == colorSeleccionado) {
                keySeleccionado = key;
                break;
            }
        }

        });
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

    $('#btn-addcarrito').click(function() {
      
        var input = $('#cantidad').val();
        console.log(idUsuario);
        var carritoData = ["|"+productoId, input, keySeleccionado].join(",");
        console.log(carritoData);

        $.ajax({
            url: '/usuarios/addcarrito',
            data: {'carritoData': carritoData, 'id': idUsuario},
            type: 'POST',
            success: function(response) {
                $('#infoProducto').modal('hide')
                var cantidadCarritoInner = parseInt($('#cantidadCarrito').text());
                cantidadCarritoInner+=1;
                $('#cantidadCarrito').hide()
                $('#cantidadCarrito').text(cantidadCarritoInner);
                $('#cantidadCarrito').style
                animateCSS('carrito', 'rotateInDownRight');
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    //ordenar productos de labios
    $('#sortA-ZLabios').on('click', function() {
        var lista = $('.productosLabios');
        lista.sort(function(a, b) {
          return $(a).data('nombre').localeCompare($(b).data('nombre'));
        });
        $('.productosLabiosContainer').empty().append(lista);
    });
    $('#sortZ-ALabios').on('click', function() {
        var lista = $('.productosLabios');
        lista.sort(function(a, b) {
          return $(b).data('nombre').localeCompare($(a).data('nombre'));
        });
        $('.productosLabiosContainer').empty().append(lista);
    });
    $('#sortPMeLabios').on('click', function() {
        var lista = $('.productosLabios');
        lista.sort(function(a, b) {
          return $(a).data('precio') - $(b).data('precio');
        });
        $('.productosLabiosContainer').empty().append(lista);
    });
    $('#sortPMaLabios').on('click', function() {
        var lista = $('.productosLabios');
        lista.sort(function(a, b) {
            return $(b).data('precio') - $(a).data('precio');
        });
        $('.productosLabiosContainer').empty().append(lista);
    });

    //ordenar productos de piel
    $('#sortA-ZPiel').on('click', function() {
        var lista = $('.productosPiel');
        lista.sort(function(a, b) {
          return $(a).data('nombre').localeCompare($(b).data('nombre'));
        });
        $('.productosPielContainer').empty().append(lista);
    });
    $('#sortZ-APiel').on('click', function() {
        var lista = $('.productosPiel');
        lista.sort(function(a, b) {
          return $(b).data('nombre').localeCompare($(a).data('nombre'));
        });
        $('.productosPielContainer').empty().append(lista);
    });
    $('#sortPMePiel').on('click', function() {
        var lista = $('.productosPiel');
        lista.sort(function(a, b) {
          return $(a).data('precio') - $(b).data('precio');
        });
        $('.productosPielContainer').empty().append(lista);
    });
    $('#sortPMaPiel').on('click', function() {
        var lista = $('.productosPiel');
        lista.sort(function(a, b) {
            return $(b).data('precio') - $(a).data('precio');
        });
        $('.productosPielContainer').empty().append(lista);
    });

    //ordenar productos para ojos
    $('#sortA-ZOjos').on('click', function() {
        var lista = $('.productosOjos');
        lista.sort(function(a, b) {
          return $(a).data('nombre').localeCompare($(b).data('nombre'));
        });
        $('.productosOjosContainer').empty().append(lista);
    });
    $('#sortZ-AOjos').on('click', function() {
        var lista = $('.productosOjos');
        lista.sort(function(a, b) {
          return $(b).data('nombre').localeCompare($(a).data('nombre'));
        });
        $('.productosOjosContainer').empty().append(lista);
    });
    $('#sortPMeOjos').on('click', function() {
        var lista = $('.productosOjos');
        lista.sort(function(a, b) {
          return $(a).data('precio') - $(b).data('precio');
        });
        $('.productosOjosContainer').empty().append(lista);
    });
    $('#sortPMaOjos').on('click', function() {
        var lista = $('.productosOjos');
        lista.sort(function(a, b) {
            return $(b).data('precio') - $(a).data('precio');
        });
        $('.productosOjosContainer').empty().append(lista);
    });

    //ordenar productos de skin
    $('#sortA-ZSkin').on('click', function() {
        var lista = $('.productosSkin');
        lista.sort(function(a, b) {
          return $(a).data('nombre').localeCompare($(b).data('nombre'));
        });
        $('.productosSkinContainer').empty().append(lista);
    });
    $('#sortZ-ASkin').on('click', function() {
        var lista = $('.productosSkin');
        lista.sort(function(a, b) {
          return $(b).data('nombre').localeCompare($(a).data('nombre'));
        });
        $('.productosSkinContainer').empty().append(lista);
    });
    $('#sortPMeSkin').on('click', function() {
        var lista = $('.productosSkin');
        lista.sort(function(a, b) {
          return $(a).data('precio') - $(b).data('precio');
        });
        $('.productosSkinContainer').empty().append(lista);
    });
    $('#sortPMaSkin').on('click', function() {
        var lista = $('.productosSkin');
        lista.sort(function(a, b) {
            return $(b).data('precio') - $(a).data('precio');
        });
        $('.productosSkinContainer').empty().append(lista);
    });

    //ordenar productos de accesorios
    $('#sortA-ZAccesorios').on('click', function() {
        var lista = $('.productosAccesorios');
        lista.sort(function(a, b) {
          return $(a).data('nombre').localeCompare($(b).data('nombre'));
        });
        $('.productosAccesoriosContainer').empty().append(lista);
    });
    $('#sortZ-AAccesorios').on('click', function() {
        var lista = $('.productosAccesorios');
        lista.sort(function(a, b) {
          return $(b).data('nombre').localeCompare($(a).data('nombre'));
        });
        $('.productosAccesoriosContainer').empty().append(lista);
    });
    $('#sortPMeAccesorios').on('click', function() {
        var lista = $('.productosAccesorios');
        lista.sort(function(a, b) {
          return $(a).data('precio') - $(b).data('precio');
        });
        $('.productosAccesoriosContainer').empty().append(lista);
    });
    $('#sortPMaAccesorios').on('click', function() {
        var lista = $('.productosAccesorios');
        lista.sort(function(a, b) {
            return $(b).data('precio') - $(a).data('precio');
        });
        $('.productosAccesoriosContainer').empty().append(lista);
    });

});

$(document).on('click', '.bi-star', function(event) {
    $(event.target).addClass('bi-star-fill');
    $(event.target).prevAll().addClass('bi-star-fill');
    $(event.target).nextAll().removeClass('bi-star-fill').removeClass('bi-star');
    $(event.target).removeClass('bi-star').addClass('bi-star-fill');
    
    var puntuacion = $('.bi-star-fill').length;
    $('input[name="puntuacion"]').val(puntuacion);
});

// Seleccionar el botón externo y la lista de pestañas
const $tabs = $('.tab');

// Agregar un controlador de eventos clic al botón externo
$(document).on('click', '.btn-opm', function(event) {
    // Obtener el índice del botón clickeado
    const index = $(event.target).data('index');
    console.log();
    // Activar la pestaña correspondiente
    $('.tab').eq(index).addClass('active').siblings().removeClass('active');
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
