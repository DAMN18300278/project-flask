$(document).ready(function() {
    // agregar un evento de escucha al campo de entrada de búsqueda
    $('#search').on('keyup', function() {
      var value = $(this).val().toLowerCase(); // obtener el valor del campo de entrada y convertirlo a minúsculas
      $('tbody tr').filter(function() { // filtrar los elementos del cuerpo de la tabla
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1); // ocultar o mostrar los elementos según el término de búsqueda
      });
    });
  });

if(window.innerHeight < window.innerWidth){
    document.location.href = '/noAdec';
}