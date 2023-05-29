$('#capture-btn').show();
$('#options').hide();
$('#optionsColors').hide();
$('#sideBarDiv').hide();

// Acceder al video y al botón de captura
const video = document.getElementById('video');

// Acceder al lienzo (canvas)
const canvas1 = document.getElementById('canvasFoto');
const canvas2 = document.getElementById('canvasResult');
const context1 = canvas1.getContext('2d');
const context2 = canvas2.getContext('2d');
var imageData = canvas1.toDataURL('image/jpeg');
let capture = true;
var cameraHeight = 0;
var cameraWidth = 0;

video.setAttribute('autoplay', '');
video.setAttribute('muted', '');
video.setAttribute('playsinline', '');

navigator.getMedia = ( 
  navigator.mediaDevices ||
  navigator.webkit ||
  navigator.mozGetUserMedia ||
  navigator.msGetUserMedia
);

// Obtener acceso a la cámara
navigator.getMedia.getUserMedia({video:true})
    .then(stream => {
        // Mostrar el flujo de la cámara en el elemento de video
        video.srcObject = stream;

        video.height = screen.height;
        video.width = screen.width;

        let stream_data = stream.getVideoTracks()[0].getSettings();
        cameraHeight = stream_data.height;
        cameraWidth = stream_data.width;
    })
    .catch(error => {
        console.error('Error al acceder a la cámara: ', error);
    });

const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebar-toggle');
const iconSidebar = document.getElementById('iconSidebar');

sidebarToggle.addEventListener('click', function() {
  sidebar.style.right = sidebar.style.right === '0%' ? '-43%' : '0%';
  sidebarToggle.style.right = sidebarToggle.style.right === '43%' ? '0' : '43%';
  iconSidebar.style.rotate = iconSidebar.style.rotate === '180deg' ? '0deg' : '180deg';

  if($('#sidebar').hasClass('active')){
    $('#optionsColors').css('z-index', '5');
    $('#sideBarDiv').css('z-index', '4');
  }else{
    $('#optionsColors').css('z-index', '4');
    $('#sideBarDiv').css('z-index', '5');
  }

  $('#sidebar').toggleClass('active');
});

// Capturar foto cuando se hace clic en el botón
$('#capture-btn').on('click', function(){
  if(capture){
    // Dibujar la imagen del video en el lienzo
    canvas1.height = cameraHeight;
    canvas1.width = cameraWidth;
    context1.drawImage(video, 0, 0, canvas1.width, canvas1.height);
    // Obtener la imagen como base64
    imageData = canvas1.toDataURL('image/jpeg');
    $('#canvasFoto').show();

    $.ajax({
      contentType: 'application/json',
      dataType: 'json',
      data: JSON.stringify({ image: imageData }),
      url: '/revisar_foto',
      type: 'post',
      success: function(response){
        if (response.Orientado){
          capture = !capture;
          // Mostrar el modal
          $('#modal-text').text("Foto tomada exitosamente!");
          $('#modal-alerts').modal('show');
          $('#capture-btn').hide();
          $('#options').show();
          $('#video').hide();
        
          // Establecer el temporizador para ocultar el modal después de 3 segundos (3000 ms)
          setTimeout(function() {
            $('#modal-alerts').modal('hide');
          }, 3000);
        }else{
          imageData = '';
          $('#canvasFoto').hide();
          $('#canvasResult').hide();
          
          // Mostrar el modal
          $('#modal-text').text("Por favor intente colocar su cabeza un poco más derecha para facilitar el sistema de probado");
          $('#modal-alerts').modal('show');
        
          // Establecer el temporizador para ocultar el modal después de 3 segundos (3000 ms)
          setTimeout(function() {
            $('#modal-alerts').modal('hide');
          }, 3000);
        }
      }
    });

  }else{
    $('#canvasFoto').hide();
    $('#canvasResult').hide();
    imageData = '0';  
    capture = !capture;
  }
});

$('#retomar').on('click', function(){
  $('#video').show();
  $('#canvasFoto').hide();
  $('#canvasResult').hide();
  $('#options').hide();
  $('#capture-btn').show();
  imageData = '0';  
  capture = !capture;
});

$('#continuar').on('click', function(){
  $.ajax({
    contentType: 'application/json',
    dataType: 'json',
    data: JSON.stringify({ image: imageData, data: initialJsonProbado }),
    url: '/procesar',
    type: 'post',
    success: function(response){
      // Mostrar la imagen procesada al usuario
      $('#canvasFoto').hide();
      const processedImage = new Image();
      processedImage.onload = function(){
        canvas2.height = cameraHeight;
        canvas2.width = cameraWidth;
        context2.drawImage(processedImage, 0, 0, canvas1.width, canvas1.height)
      }
      processedImage.src = 'data:image/png;base64,' + response.processedImageUrl;
      $('#canvasResult').show();
      $('#options').hide();
      $('#sideBarDiv').show();
      $('#optionsColors').show();
      $('.filter').first().click();
    }
  });

});

function actualizarFrame() {
  $.ajax({
    contentType: 'application/json',
    dataType: 'json',
    data: JSON.stringify({ image: imageData, data: initialJsonProbado }),
    url: '/procesar',
    type: 'post',
    success: function(response){
      // Mostrar la imagen procesada al usuario
      $('#canvasFoto').hide();
      const processedImage = new Image();
      processedImage.onload = function(){
        canvas2.height = cameraHeight;
        canvas2.width = cameraWidth;
        context2.drawImage(processedImage, 0, 0, canvas1.width, canvas1.height)
      }
      processedImage.src = 'data:image/png;base64,' + response.processedImageUrl;
    }
  });
}

$(document).on('click', '.filter', function() {
  // Elimina la clase 'active' de todos los filtros
  $('.filter').removeClass('active');
  $('.filter').css({ 'width': '40px', 'height': '40px' });

  // Agrega la clase 'active' al filtro seleccionado
  $(this).addClass('active').css({ 'width': '60px', 'height': '60px' });

  // Calcula el desplazamiento necesario para centrar el filtro seleccionado
  const containerWidth = $('.filter-slider').outerWidth();
  const filterPosition = $(this).position().left;
  const translateX = containerWidth / 2 - filterPosition - $(this).outerWidth() / 2;

  // Aplica el desplazamiento al filtro slider utilizando animación
  $('.filter-slider').animate({ 'left': translateX }, 300); 

  var splitJson = initialJsonProbado.split(',');
  var eachSplit = splitJson[initialPart].split(':');
  
  splitJson[initialPart] = `${eachSplit[0]}:${$(this).data('color')}`;

  initialJsonProbado = splitJson.join(',')
  actualizarFrame();
});

$(document).ready(function () {

  $('.productLabios').on('click', function() {
    if($(this).hasClass('border-danger')){
      $('.productLabios').removeClass('border-danger box-shadow1');
      var splitJson = initialJsonProbado.split(',');
      splitJson[0] = "0:0";
      initialJsonProbado = splitJson.join(',');
      $('.filter-slider').empty();

      actualizarFrame();
      return;
    }
    $('.productLabios').removeClass('border-danger box-shadow1');
    $(this).addClass('border-danger box-shadow1');
    initialPart = 0;

    var splitJson = initialJsonProbado.split(',');
    splitJson[0] = $(this).data('id') + ":1";
    initialJsonProbado = splitJson.join(',');

    actualizarFrame();
    
    var sinComillas = $(this).data('colores').replace('\n\n', " ");
    var sinTabs = sinComillas.replace(/'/g, "\"");

    var jsonColores = JSON.parse(sinTabs);
    var replace = "";

    for (let i = 1; i <= Object.keys(jsonColores).length; i++) {
      const element = jsonColores[i.toString()];
      replace += `<div class="filter" data-color="${i}" style="background-color: #${element['Hex']};"></div>`
    }

    $('.filter-slider').empty().append(replace);
    $('.filter').first().trigger('click');
    
    setTimeout(() => {
      $('#sidebar-toggle').trigger('click');
    }, 600);
  });
  
  $('.productSombras').on('click', function() {
    if($(this).hasClass('border-danger')){
      $('.productSombras').removeClass('border-danger box-shadow1');
      var splitJson = initialJsonProbado.split(',');
      splitJson[2] = "0:0";
      initialJsonProbado = splitJson.join(',');
      $('.filter-slider').empty();
      
      actualizarFrame();
      return;
    }
    $('.productSombras').removeClass('border-danger box-shadow1');
    $(this).addClass('border-danger box-shadow1');
    initialPart = 2;

    var splitJson = initialJsonProbado.split(',');
    splitJson[2] = $(this).data('id') + ":1";
    initialJsonProbado = splitJson.join(',');

    actualizarFrame();
    
    var sinComillas = $(this).data('colores').replace('\n\n', " ");
    var sinTabs = sinComillas.replace(/'/g, "\"");

    var jsonColores = JSON.parse(sinTabs);
    var replace = "";

    for (let i = 1; i <= Object.keys(jsonColores).length; i++) {
      const element = jsonColores[i.toString()];
      replace += `<div class="filter" data-color="${i}" style="background-color: #${element['Hex']};"></div>`
    }

    $('.filter-slider').empty().append(replace);
    $('.filter').first().trigger('click');
    
    setTimeout(() => {
      $('#sidebar-toggle').trigger('click');
    }, 600);
  })
  
  $('.productPestañas').on('click', function() {
    if($(this).hasClass('border-danger')){
      $('.productPestañas').removeClass('border-danger box-shadow1');
      var splitJson = initialJsonProbado.split(',');
      splitJson[1] = "0";
      initialJsonProbado = splitJson.join(',');
      $('.filter-slider').empty();
      
      actualizarFrame();
      return;
    }
    $('.productPestañas').removeClass('border-danger box-shadow1');
    $(this).addClass('border-danger box-shadow1');
    initialPart = 1;

    var splitJson = initialJsonProbado.split(',');
    splitJson[1] = $(this).data('id');
    initialJsonProbado = splitJson.join(',');

    actualizarFrame();
    
    var sinComillas = $(this).data('colores').replace('\n\n', " ");
    var sinTabs = sinComillas.replace(/'/g, "\"");

    var jsonColores = JSON.parse(sinTabs);
    var replace = "";

    for (let i = 1; i <= Object.keys(jsonColores).length; i++) {
      const element = jsonColores[i.toString()];
      replace += `<div class="filter" data-color="${i}" style="background-color: #${element['Hex']};"></div>`
    }

    $('.filter-slider').empty().append(replace);
    $('.filter').first().trigger('click');

    setTimeout(() => {
      $('#sidebar-toggle').trigger('click');
    }, 600);
  })
})