$('#options').hide();
$('#options2').hide();

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

// Capturar foto cuando se hace clic en el botón
$('#capture-btn').on('click', function(){
  if(capture){
    // Dibujar la imagen del video en el lienzo
    canvas1.height = cameraHeight;
    canvas1.width = cameraWidth;
    context1.drawImage(video, 0, 0, canvas1.width, canvas1.height);
    // Obtener la imagen como base64
    imageData = canvas1.toDataURL('image/jpeg');3
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
    data: JSON.stringify({ image: imageData }),
    url: '/procesarRostro',
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
        $('#continuar').text(response.Forma);
    }
  });
});