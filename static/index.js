correo = document.getElementById("correo")
        contraseña = document.getElementById("contraseña")
        contraseñaC = document.getElementById("contraseñaC")
        alerta = document.getElementById("alerta")
        msg = document.getElementById("msg")
        titulo = document.getElementById("tituloMsg")

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