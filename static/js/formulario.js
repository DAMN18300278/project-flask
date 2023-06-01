rsMark = document.getElementById("rs-mark");
slider = document.getElementById("edad");
alertaOjos = document.getElementById("alertaOjos");
alertaPiel = document.getElementById("alertaPiel");
alertaColorPiel = document.getElementById("alertaColorPiel");
alertaColorPelo = document.getElementById("alertaColorPelo");
alertaAlergias = document.getElementById("alertaAlergias");
valorOjos = document.getElementById("colorOjos");
btnTipoPiel = document.getElementById("btnTipoPiel");
btnColorOjos = document.getElementById("btnColorOjos");
btnColorPiel = document.getElementById("inputColorPiel");
divColorPiel = document.getElementById("divColorPiel");
btnColorCabello = document.getElementById("inputColorCabello");
divColorCabello = document.getElementById("divColorCabello");

slider.addEventListener("input", showSliderValue, true);
document.addEventListener("DOMContentLoaded", showSliderValue);

function showSliderValue(){
    rsMark.innerHTML = slider.value;
    var position = (slider.value / slider.max);
    rsMark.style.left = (position * 85) + "%";
}

function selectEyes(){
    alertaOjos.style.display = "block";
}
function selectAlergias(){
    alertaAlergias.style.display = "block";
}

function selectSkin(){
    alertaPiel.style.display = "block";
}

function colorOjos(index){
    valorOjos.value = index;
    if(index == 1){
        btnColorOjos.style.backgroundColor = "#202020"
        btnColorOjos.style.color = "#fff"
        btnColorOjos.textContent = "Color de ojos: Negro"

    }else if(index == 2){
        btnColorOjos.style.backgroundColor = "#563330"
        btnColorOjos.style.color = "#fff"
        btnColorOjos.textContent = "Color de ojos: Café"

    }else if(index == 3){
        btnColorOjos.style.backgroundColor = "#aaa24e"
        btnColorOjos.style.color = "#000"
        btnColorOjos.textContent = "Color de ojos: Amarillo"

    }else if(index == 4){
        btnColorOjos.style.backgroundColor = "#9ca194"
        btnColorOjos.style.color = "#000"
        btnColorOjos.textContent = "Color de ojos: Gris"

    }else if(index == 5){
        btnColorOjos.style.backgroundColor = "#abc6d0"
        btnColorOjos.style.color = "#000"
        btnColorOjos.textContent = "Color de ojos: Azul"

    }else if(index == 6){
        btnColorOjos.style.backgroundColor = "#31684c"
        btnColorOjos.style.color = "#fff"
        btnColorOjos.textContent = "Color de ojos: Verde"
    }
    alertaOjos.style.display = "none";
}

function textoPiel(index){
    btnTipoPiel.textContent = "Tipo de piel: " + index;
    alertaPiel.style.display = "none";
}

function colorPiel(val, color){
    $('#inputColorPielForm').val(color.replace("#", ""))
    $('#inputColorPiel').val(val.replace("#", ""))
    divColorPiel.style.backgroundColor = color;
    alertaColorPiel.style.display = "none";
}

function colorPelo(val, color){
    btnColorCabello.value = val.replace("#", "");
    divColorCabello.style.backgroundColor = color;
    alertaColorPelo.style.display = "none";
}