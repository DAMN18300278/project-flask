rsMark = document.getElementById("rs-mark");
slider = document.getElementById("edad");
alerta = document.getElementById("alertaOjos");
valorOjos = document.getElementById("colorOjos");

slider.addEventListener("input", showSliderValue, true);
document.addEventListener("DOMContentLoaded", showSliderValue);

function showSliderValue(){
    rsMark.innerHTML = slider.value;
    var position = (slider.value / slider.max);
    rsMark.style.left = (position * 85) + "%";
}

function selectEyes(){
    alerta.style.display = "block";
}

function colorOjos(index){
    valorOjos.value = index;
    alerta.style.display = "none";
}