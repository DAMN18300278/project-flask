var alerta;
var modalAlerta;

document.addEventListener("DOMContentLoaded", () => {
    var url = $(location).attr('href')
    if(!url.includes('formulario')){
        horizontalMenuChange(1);
    }

    alerta = document.getElementById('alertaRed');
    modalAlerta = bootstrap.Modal.getOrCreateInstance(alerta);
    verificarConexion();
});


function verificarConexion() {
    $.ajax({
        url: "https://api.ipify.org?format=json",
        type: "GET",
        success: function() {
            modalAlerta.hide();
        },
        error: function() {
            modalAlerta.show();
        },
        complete: function() {
          setTimeout(verificarConexion, 3500);
        }
    });
}

if(window.innerHeight < window.innerWidth){
    document.location.href = '/noAdec';
}

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
    var originalItemsOjos = $("#dropdownSearchProductsAddPubList").find("#itemAddPub[data-nombre]").clone();
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
    $("#dropdownSearchProductsPub").keyup(function() {
        var filter = $(this).val().toLowerCase();
        var items = $("#dropdownSearchProductsAddPubList").find("#itemAddPub[data-nombre], #itemAddPub[data-id]");
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
    
    var timeoutId;

    $('#infoProducto').on('show.bs.modal', function(event){
        var boton = $(event.relatedTarget);
        var modal = $(this);

        var alergias = boton.data('alergias');
        console.log(alergias)
        var ingredientesString = boton.data('ingredientes')
        
        var ingredientes = ingredientesString.split('|');
        console.log(ingredientes)
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
        var categoria = productJson['Categoria'];
        var nombre = productJson['Nombre'];
        var descripcion = productJson['Descripcion'];
        var tipoPiel = productJson['Tipo de piel'];
        var colores = productJson['Colores'];
        var marca = productJson['Marca'];
        var tipo = productJson['Tipo'];
        var stock = productJson['Stock'];
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


        var indice = alergias.indexOf(productoId);
        console.log(indice)
        if (indice != -1) {
            modal.find('#alergiasInfoProductos').text("El producto contiene ingredientes como: "+ingredientes[indice]+". Le recomendamos que use este producto con precaucion debido a sus alergias").show();
        } else {
           
            modal.find('#alergiasInfoProductos').hide();
        }
        
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
        modal.find('#cantidad').prop('max', stock)

        modal.find('#hexColorInfoProductos').find('.colores-info').first().trigger('click');

        if (tipo.toString().toLowerCase().includes('labial') ||
            tipo.toString().toLowerCase().includes('pestaña') ||
            tipo.toString().toLowerCase().includes('sombra') ||
            tipo.toString().toLowerCase().includes('gloss')){
                var link;
            
                switch (categoria) {
                    case 'labios':
                        link = productoId + ":1,0,0:0"
                        break;
                        
                    case 'ojos':
                        if(tipo.toString().toLowerCase().includes('pestaña')){
                            link = "0:0," + productoId + ",0:0"
                        }else{
                            link = "0:0,0," + productoId + ":1"
                        }
                        break;
                }
                var inner = "<a type='button' class='btn btn-danger me-auto px-4 py-2 d-flex align-items-center' style='border-radius: 0px; font-size:15px' href='\\usuarios\\probado\\" + link + "' id='btnProbar'>Probar</a>"
                $('#btn-addcarrito').before(inner);
        }else{
            var inner = "<button type='button' class='btn btn-danger me-auto px-4 py-2 d-flex align-items-center' data-bs-dismiss='modal' style='border-radius: 0px; font-size:15px' id='btnProbar'>Cancelar</button>"
            $('#btn-addcarrito').before(inner);
        }
    
        timeoutId = setTimeout(() => {            
            $.ajax({
                url: '/actualizarvistas',
                contentType: 'application/json',
                type: 'POST',
                data: JSON.stringify({ productoid: productoId }),
                dataType: 'json',
                success: function(response) {
                    console.log(response);
                },
                error: function(error) {
                    console.log(error);
                }
            });
        }, 3000);

        var inner = "";
        $.ajax({
            url: '/usuarios/conjunto',
            contentType: 'application/json',
            type: 'POST',
            data: JSON.stringify({ productoid: productoId }),
            dataType: 'json',
            success: function(response) {
                $('#conjuntos').empty();
                if(response.length > 0){

                    let count = 1;
                    response.forEach(element => {
                        if(count < 7){
                            $.ajax({
                                url: `/productsApi/${element}`,
                                type: 'GET',
                                success: function (response2){
                                    var producto = response2['Productos'][0];
                                    var imgInner = `static/src/img${element}_1.jpg`;
                                    inner += 
                                    `<div class="w-50 mx-3">
                                        <div class="border border-1 box-shadow1 position-relative productConjunto"
                                        data-bs-toggle="modal"
                                        data-
                                        data-bs-target="#infoProducto" 
                                        data-producto="${JSON.stringify(producto)}"
                                        onclick="$('#infoProducto').modal('show')"
                                        data-alergias="${alergias}"
                                        data-ingredientes="${ingredientes}" style="width:6.5em; height:6.5em;">
                                            <img src="${imgInner}" style="width:6em; height:6em;">
                                            <div class="position-absolute border border-danger bg-white py-1 px-2" style="bottom: 5%; left: 5%; overflow:hidden; max-width:90%">
                                                <p class="mb-0 text-start" style="font-size: 9px;letter-spacing:1px;white-space:break-spaces">${producto['Nombre']}</p>
                                                <p class="mb-0 text-start" style="font-size: 8px;letter-spacing:1px;font-weight: bold;">$${producto['Precio u.']}</p>
                                            </div>
                                        </div>
                                    </div>`;
                                    $('#conjuntos').html(inner);
                                },
                                error: function (error) {
                                    console.log(error);
                                }
                            });
                        }
                    count++;
                });
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
    
    $('#infoProducto').on('hidden.bs.modal', function(){
        clearTimeout(timeoutId);
        var modal = $(this);
        modal.find('#cantidad').val(1);
        modal.find('#nombreColorInfoProductos').text('Color');
        $('#btnProbar').remove()
    });


    $('#infokit').on('show.bs.modal', function(event){
        const button = event.relatedTarget; // elemento que dispara el modal
        const productos = button.getAttribute('data-producto'); // JSON principal
        const Labios = button.getAttribute('data-productos-labios'); // JSON de labios
        const Piel = button.getAttribute('data-productos-piel'); // JSON de piel
        const Ojos =button.getAttribute('data-productos-ojos'); // JSON de ojos
        const SkinCare = button.getAttribute('data-productos-skincare'); // JSON de cuidado de piel
        const Accesorios = button.getAttribute('data-productos-accesorios');

        // // haz algo con los arreglos, por ejemplo:
        var modal = $(this);
        
        const labiosconcomillas = Labios.replace(/'/g, '"');
        const productosLabios = JSON.parse(labiosconcomillas);

        const pielconcomillas = Piel.replace(/'/g, '"');
        const productosPiel = JSON.parse(pielconcomillas);

        const ojosconcomillas = Ojos.replace(/'/g, '"');
        const productosOjos = JSON.parse(ojosconcomillas);

        const skincareconcomillas = SkinCare.replace(/'/g, '"');
        const productosSkinCare = JSON.parse(skincareconcomillas);

        const accesoriosconcomillas = Accesorios.replace(/'/g, '"');
        const productosAccesorios = JSON.parse(accesoriosconcomillas);

        let indexcoloraccesorios = 1;
        let indexcolorojos = 1;
        let indexcolorpiel = 1;
        let indexcolorlabios = 1;
        let indexcolorskincare = 1;

        //Accesorios
        modal.find('#imagenaccesorios').attr('src', '../static/src/img'+productosAccesorios['Id']+'_1.jpg');
        modal.find('#nombreprodaccesorios').text(productosAccesorios['Nombre']);
        modal.find('#precioprodaccesorios').text(productosAccesorios['Precio u.']);
        modal.find('#stockaccesorios').text(productosAccesorios['Stock'] + " disponibles");
        modal.find('#colorhexaccesorios').css('background-color','#'+productosAccesorios.Colores[indexcoloraccesorios].Hex);

        //Ojos
        modal.find('#imagenojos').attr('src', '../static/src/img'+productosOjos['Id']+'_1.jpg');
        modal.find('#nombreprodojos').text(productosOjos['Nombre']);
        modal.find('#precioprodojos').text(productosOjos['Precio u.']);
        modal.find('#stockojos').text(productosOjos['Stock'] + " disponibles");
        modal.find('#colorhexojos').css('background-color','#'+productosOjos.Colores[indexcolorojos].Hex);

        //Piel
        modal.find('#imagenpiel').attr('src', '../static/src/img'+productosPiel['Id']+'_1.jpg');
        modal.find('#nombreprodpiel').text(productosPiel['Nombre']);
        modal.find('#precioprodpiel').text(productosPiel['Precio u.']);
        modal.find('#stockpiel').text(productosPiel['Stock'] + " disponibles");
        modal.find('#colorhexpiel').css('background-color','#'+productosPiel.Colores[indexcolorpiel].Hex);

        //Labios
      
        modal.find('#imagenlabios').attr('src', '../static/src/img'+productosLabios['Id']+'_1.jpg');
        modal.find('#nombreprodlabios').text(productosLabios['Nombre']);
        modal.find('#precioprodlabios').text(productosLabios['Precio u.']);
        modal.find('#stocklabios').text(productosLabios['Stock'] + " disponibles");
        modal.find('#colorhexlabios').css('background-color','#'+productosLabios.Colores[indexcolorlabios].Hex);

        //Skin Care
        modal.find('#imagenskincare').attr('src', '../static/src/img'+productosSkinCare['Id']+'_1.jpg');
        modal.find('#nombreprodskincare').text(productosSkinCare['Nombre']);
        modal.find('#precioprodskincare').text(productosSkinCare['Precio u.']);
        modal.find('#stockskincare').text(productosSkinCare['Stock'] + " disponibles");
        modal.find('#colorhexskincare').css('background-color','#'+productosSkinCare.Colores[indexcolorskincare].Hex);

        $('#infokit').data('id-ojos', productosOjos['Id']);
        
        let String = "|"+productosOjos['Id'] + ',1,' + indexcolorojos + '|' + 
            productosPiel['Id'] + ',1,' + indexcolorpiel + '|' + 
            productosLabios['Id'] + ',1,' + indexcolorlabios + '|' + 
            productosSkinCare['Id'] + ',1,' + indexcolorskincare + '|' + 
            productosAccesorios['Id'] + ',1,' + indexcoloraccesorios;
        
        const btnAddCarrito = document.querySelector('#btn-kit');
        btnAddCarrito.addEventListener('click', function() {

            fetch('/usuarios/addcarrito', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
                },
            body: 'carritoData=' + encodeURIComponent(String)
            })
              .then(response => {
                console.log('Respuesta del servidor:', response);
            })
              .catch(error => {
                console.error('Error al enviar la solicitud:', error);
            });   
        });
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
    var max = parseInt(input.attr('max')); // Obtener el valor de max
    if (value < max || isNaN(max)) { // Verificar si value es menor a max
        input.val(value + 1);
    }
    });

    $('#btn-addcarrito').click(function() {
      
        var input = $('#cantidad').val();
        var carritoData = ["|"+productoId, input, keySeleccionado].join(",");

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
                $('#cantidadCarrito').show()
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
    $('#sortColorsLabios').on('click', function() {
        var lista = $('.productosLabios');
        lista.sort(function(a, b) {
            var primerColor = $(a).data('color');
            var segundoColor = $(b).data('color');
            
            // Compara los códigos hexadecimales
            if (primerColor > segundoColor) {
                return -1;
            } else if (primerColor < segundoColor) {
                return 1;
            } else {
                return 0;
            }
        });
        $('.productosLabiosContainer').empty().append(lista);
    });
    $('#sortPielLabios').on('click', function() {
        var lista = $('.productosLabios');
        lista.sort(function(a, b) {
            return $(a).data('piel') - $(b).data('piel');
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
    $('#sortColorsPiel').on('click', function() {
        var lista = $('.productosPiel');
        lista.sort(function(a, b) {
            var primerColor = $(a).data('color');
            var segundoColor = $(b).data('color');
            
            // Compara los códigos hexadecimales
            if (primerColor > segundoColor) {
                return -1;
            } else if (primerColor < segundoColor) {
                return 1;
            } else {
                return 0;
            }
        });
        $('.productosPielContainer').empty().append(lista);
    });
    $('#sortPielPiel').on('click', function() {
        var lista = $('.productosPiel');
        lista.sort(function(a, b) {
            return $(a).data('piel') - $(b).data('piel');
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
    $('#sortColorsOjos').on('click', function() {
        var lista = $('.productosOjos');
        lista.sort(function(a, b) {
            var primerColor = $(a).data('color');
            var segundoColor = $(b).data('color');
            
            // Compara los códigos hexadecimales
            if (primerColor > segundoColor) {
                return -1;
            } else if (primerColor < segundoColor) {
                return 1;
            } else {
                return 0;
            }
        });
        $('.productosOjosContainer').empty().append(lista);
    });
    $('#sortPielOjos').on('click', function() {
        var lista = $('.productosOjos');
        lista.sort(function(a, b) {
            return $(a).data('piel') - $(b).data('piel');
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
    $('#sortColorsSkin').on('click', function() {
        var lista = $('.productosSkin');
        lista.sort(function(a, b) {
            var primerColor = $(a).data('color');
            var segundoColor = $(b).data('color');
            
            // Compara los códigos hexadecimales
            if (primerColor > segundoColor) {
                return -1;
            } else if (primerColor < segundoColor) {
                return 1;
            } else {
                return 0;
            }
        });
        $('.productosSkinContainer').empty().append(lista);
    });
    $('#sortPielSkin').on('click', function() {
        var lista = $('.productosSkin');
        lista.sort(function(a, b) {
            return $(a).data('piel') - $(b).data('piel');
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
    $('#sortColorsAccesorios').on('click', function() {
        var lista = $('.productosAccesorios');
        lista.sort(function(a, b) {
            var primerColor = $(a).data('color');
            var segundoColor = $(b).data('color');
            
            // Compara los códigos hexadecimales
            if (primerColor > segundoColor) {
                return -1;
            } else if (primerColor < segundoColor) {
                return 1;
            } else {
                return 0;
            }
        });
        $('.productosAccesoriosContainer').empty().append(lista);
    });
    $('#sortPielAccesorios').on('click', function() {
        var lista = $('.productosAccesorios');
        lista.sort(function(a, b) {
            return $(a).data('piel') - $(b).data('piel');
        });
        $('.productosAccesoriosContainer').empty().append(lista);
    });

});

// $(document).on('click', '.productConjunto', function(){
//     $('#infoProducto').modal('hide');
//     console.log($(this));
//     setTimeout(() => {
//         $(this).trigger('data-bs-toggle');
//     }, 1000)
// });

$(document).on('click', '.star', function(event) {
    $items = $('.star')
    $($items).removeClass('starSelected')
    $($items).removeClass('bi-star-fill').removeClass('bi-star')
    $(event.target).addClass('bi-star-fill');
    $(event.target).addClass('starSelected');
    $(event.target).prevAll().addClass('bi-star-fill');
    $(event.target).prevAll().addClass('starSelected');
    $(event.target).nextAll().addClass('bi-star');
    
    var puntuacion = $('.starSelected').length;
    $('input[name="puntuacion"]').val(puntuacion);
    console.log($('input[name="puntuacion"]').val());

});

$(document).ready(function () {
    var page_num = 1;

    $('.nav-link').on('click', function(){
        page_num = $(this).data('idnav');
    });

    $('.productAddPub').click(function () {
        const idProducto = $(this).data('id');
        const nombre = $(this).data('nombre');
        
        $('#nombreProductoAddPub').val(nombre+ " #" + idProducto)
        $('#idProductoAddPub').val(idProducto)
    })

    $('#publicar').click(function () {
        const idProducto = $('#idProductoAddPub').val();
        const descripcion = $('#descripcionAddPub').val();
        const puntuacion = $('#puntuacionAddPub').val();

        $.ajax({
            url: '/usuarios/guardarPub',
            data: {'Id_producto': idProducto, 'Descripcion': descripcion, 'Puntuacion': puntuacion},
            type: 'POST',
            success: function (response) {
                $('#crearPub').modal('hide');
                const alerta = $('<div class="alert animate__animated animate__fadeInDown" style="color: #810CA8; background-color: #F0D9FF" role="alert">Publicación creada exitosamente !</div>');
                $('#alertas').append(alerta);
                setTimeout(function () {
                    location.reload()
                }, 2500);
            },
            error: function(error){
                console.log(error);
            }
        })
    })

    var itemsCopy = $('.pubListItem');
    $("#searchPubs").keyup(function() {
        var filter = $(this).val().toLowerCase();
        var items = $('.pubListItem');
        if (filter.length == 0) {
            $(`#content1 #pubList`).empty();
            let pageIndex = 0;
            for (let i = 0; i < itemsCopy.length; i++) {
                if (i % 5 == 0) {
                    pageIndex++;
                }
                $(`#content${pageIndex} #pubList`).append(itemsCopy[i]);
            }
        } else {
            $('.tab-pane .pubListItem').appendTo(`#content1 #pubList`);
            $(`#content1 #pubList`).empty();
            items.each(function() {
                var productName = $(this).data("nombre-producto").toLowerCase();
                var userName = $(this).data("nombre-usuario").toLowerCase();
                var id = $(this).data("id-producto");
                var match = productName.indexOf(filter) > -1 || userName.indexOf(filter) > -1 || id.toString().indexOf(filter) > -1;
                if (match) {
                    $(this).appendTo(`#content1 #pubList`);
                }
            });
        }
    });
    

    //ordenar productos de accesorios
    $('#sortDate').on('click', function() {
        var lista = $('.pubListItem');
        var fechaActual = new Date(); // obtener la fecha actual
        lista.sort(function(a, b) {
            var fechaA = new Date($(a).data('fecha-publicacion'));
            var fechaB = new Date($(b).data('fecha-publicacion'));
            var diferenciaA = fechaActual - fechaA; // calcular la diferencia de fecha actual a fechaA
            var diferenciaB = fechaActual - fechaB; // calcular la diferencia de fecha actual a fechaB
            return diferenciaA - diferenciaB; // ordenar por la diferencia desde la más reciente a la más vieja
        });
        let pageIndex = 0;
        $(' #pubList').empty()
        for (let i = 0; i < lista.length; i++) {
            if(i % 5 == 0){
                pageIndex++;
            }
            $(`#content${pageIndex} #pubList`).append(lista[i]);
        }

        itemsCopy = lista;
    });
      
      $('#sortBestRated').on('click', function() {
        var lista = $('.pubListItem');
        lista.sort(function(a, b) {
            return $(b).data('calificacion') - $(a).data('calificacion');
        });
        let pageIndex = 0;
        $(' #pubList').empty()
        for (let i = 0; i < lista.length; i++) {
            if(i % 5 == 0){
                pageIndex++;
            }
            $(`#content${pageIndex} #pubList`).append(lista[i]);
        }
        itemsCopy = lista;
    });
      
    $('#sortWorstRated').on('click', function() {
        var lista = $('.pubListItem');
        lista.sort(function(a, b) {
            return $(a).data('calificacion') - $(b).data('calificacion');
        });
        let pageIndex = 0;
        $(' #pubList').empty()
        for (let i = 0; i < lista.length; i++) {
            if(i % 5 == 0){
                pageIndex++;
            }
            $(`#content${pageIndex} #pubList`).append(lista[i]);
        }
        itemsCopy = lista;
    });
      
    $('#sortId').on('click', function() {
        var lista = $('.pubListItem');
        lista.sort(function(a, b) {
            return $(a).data('id-producto') - $(b).data('id-producto');
        });
        let pageIndex = 0;
        $(' #pubList').empty()
        for (let i = 0; i < lista.length; i++) {
            if(i % 5 == 0){
                pageIndex++;
            }
            $(`#content${pageIndex} #pubList`).append(lista[i]);
        }
        itemsCopy = lista;
    });

    $('#sortBrand').on('click', function() {
        var lista = $('.pubListItem');
        lista.sort(function(a, b) {
            return $(a).data('marca').localeCompare($(b).data('marca'));
        });
        let pageIndex = 0;
        $(' #pubList').empty()
        for (let i = 0; i < lista.length; i++) {
            if(i % 5 == 0){
                pageIndex++;
            }
            $(`#content${pageIndex} #pubList`).append(lista[i]);
        }
        itemsCopy = lista;
    });
      
    $('#sortCategorie').on('click', function() {
        var lista = $('.pubListItem');

        lista.sort(function(a, b) {
            return $(a).data('categoria').localeCompare($(b).data('categoria'));
        });

        let pageIndex = 0;
        $(' #pubList').empty()
        for (let i = 0; i < lista.length; i++) {
            if(i % 5 == 0){
                pageIndex++;
            }
            $(`#content${pageIndex} #pubList`).append(lista[i]);
        }
        itemsCopy = lista;
    });
})
// Seleccionar el botón externo y la lista de pestañas
const $tabs = $('.tab');

// Agregar un controlador de eventos clic al botón externo
$(document).on('click', '.btn-opm', function(event) {
    // Obtener el índice del botón clickeado
    const index = $(event.target).data('index');
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
    }

    node.addEventListener('animationend', handleAnimationEnd, {once: true});
});
