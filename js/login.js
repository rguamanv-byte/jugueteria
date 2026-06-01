    async function iniciarSesion(){

        const usuario = document.getElementById("usuario").value;
        const password = document.getElementById("password").value;

        const mensaje = document.getElementById("mensajeLogin");

        mensaje.innerHTML = "";

        try{

            const response = await fetch("https://jugueteria-backend.onrender.com/login",{

                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body: JSON.stringify({
                    usuario: usuario,
                    password: password
                })

            });

            const data = await response.json();

            if(data.ok){

                alert("Bienvenido " + usuario);

                location.reload();

            }else{

                mensaje.innerHTML = "Usuario o contraseña incorrectos";

            }

        }catch(error){

            mensaje.innerHTML = "Error de conexión con el servidor";

        }

    }

