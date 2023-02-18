correo = document.getElementById("correo")
correoreco = document.getElementById("correorecover")
contraseña = document.getElementById("contraseña")
contraseñaC = document.getElementById("contraseñaC")
alerta = document.getElementById("alerta")
msg = document.getElementById("msg")
titulo = document.getElementById("tituloMsg")

const campos = {
    contraseña: false,
    contraseñaC: false
}
const formulario = document.getElementById("formcambiarcontra");
const contraA = document.querySelector("#contraseña")
const contraB = document.querySelector("#contraseñaC")


const expresiones = {
    usuario: /^[a-zA-Z0-9\_\-]{4,16}$/, // Letras, numeros, guion y guion_bajo
    nombre: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, // Letras y espacios, pueden llevar acentos.
    password: /^.{4,12}$/, // 4 a 12 digitos.
    correo: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
    telefono: /^\d{7,14}$/ // 7 a 14 numeros.
}

const ValidarForm = (e) => {
    switch(e.target.name) {
        case "contraseña":
            if(expresiones.password.test(e.target.value)){
                errorcontra1.textContent = ""
                campos[contraseñaC] = true;
            }else{
                errorcontra1.textContent = "La contraseña tiene que ser de 4 a 12 digitos"
                campos[contraseña] = false;
            }
            
            validarPass2();

            break;
            case "contraseñaC":
            validarPass2();
            break;
    }

}

const validarPass2 = () => {
    if(contraseña.value !== contraseñaC.value){
        errorcontra2.textContent = "Las contraseñas no coinciden"
        campos[contraseñaC] = false;
    }else{
        errorcontra2.textContent = ""
        campos[contraseñaC] = true;
    }
}

contraA.addEventListener('keyup', ValidarForm);
contraB.addEventListener('keyup', ValidarForm); 

function button_cambiarcontra(){
    if(contraseña.value == contraseñaC.value){
        document.getElementById("formcambiarcontra").submit()
    }else{
        alert('error');
    }
}

function button_recover(){
    var expReg= /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/;
    let correoRec = correoreco.value
    let esvalido = expReg.test(correoRec)

    if(esvalido ==true){
        document.getElementById("formrecover").submit()
    }
    else{
        msg.textContent = "Este es un correo invalido"
    }

}

function button() {
    let correoEnc = correo.value
    var posAt

    if(correoEnc.indexOf('@') > 4){
        posAt = correoEnc.indexOf('@') - 4
    }else{
        titulo.textContent = "Correo invalido"
        msg.textContent = "Este no es un correo valido"
    }

    correoEnc = correoEnc.replace(correoEnc.substr(4, posAt), '*'.repeat(posAt))

    if(contraseña.value == contraseñaC.value && posAt != null && contraseña.value != ""){
        titulo.textContent = "Confirmar contraseña"
        msg.textContent = "Confirme su cuenta ingresando al link enviado al correo " + correoEnc
    }else if(posAt != null){
        titulo.textContent = "Contraseña invalida"
        msg.textContent = "Debe de ingresar una contraseña"
    }else{
        titulo.textContent = "Correo invalido"
        msg.textContent = "Este no es un correo valido"
    }

    alerta.style.display = "block"
}

function index() {
    if(titulo.textContent == "Confirmar contraseña"){
        document.getElementById("form").submit()
    }else{
        alerta.style.display = "none"
    }
}