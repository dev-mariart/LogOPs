document.addEventListener("DOMContentLoaded", function() {
    const numeroEmpleado = document.getElementById("dashboard-container").getAttribute("data-numero-empleado");

   
    function mostrarMensajeError() {
        const errorMessageElement = document.getElementById("error-message");
        errorMessageElement.textContent = "You have already clocked in today.";
        errorMessageElement.style.display = "block"; 
        setTimeout(function() {
            errorMessageElement.style.display = "none"; 
        }, 3000); 
    }


    function mostrarMensajeExitoso(tipo) {
        const successMessageElement = document.getElementById("success-message");
        const tipoMarcaTexto = obtenerNombreTipoMarca(tipo);
        successMessageElement.textContent = `Mark of ${tipoMarcaTexto} registered successfully.`;
        successMessageElement.style.display = "block"; 
        setTimeout(function() {
            successMessageElement.style.display = "none"; 
        }, 3000); 
    }

    
    function obtenerNombreTipoMarca(tipo) {
        const nombres = {
            "entrada": "start of shift",
            "descanso": "break time",
            "regreso_descanso": "return from break",
            "fin_turno": "end of shift"
        };
        return nombres[tipo];
    }

    
    function formatDateTime(date) {
        const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
        const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

        const dayOfWeek = daysOfWeek[date.getDay()];
        const dayOfMonth = date.getDate();
        const month = months[date.getMonth()];
        const year = date.getFullYear();
        const hours = date.getHours() > 12 ? date.getHours() - 12 : date.getHours();
        const minutes = date.getMinutes().toString().padStart(2, '0');
        const amPm = date.getHours() >= 12 ? 'PM' : 'AM';

        return `${dayOfWeek} ${dayOfMonth}, ${month} at ${year} - ${date.getHours()}:${minutes}:${date.getSeconds()} ${amPm}`;
    }

    
    function updateCurrentDateTime() {
        const currentDateTimeElement = document.getElementById("current-datetime");
        const currentDate = new Date();
        const formattedDateTime = formatDateTime(currentDate);
        currentDateTimeElement.textContent = `${formattedDateTime}`;
    }

    
    updateCurrentDateTime();

   
    setInterval(updateCurrentDateTime, 1000);

    
    function marcar(tipo) {
        const fechaHoraMarca = moment().format("YYYY-MM-DD HH:mm:ss");
        fetch(`/marcar/${numeroEmpleado}/${tipo}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ fecha_hora_marca: fechaHoraMarca })
        })
            .then(response => {
                if (response.ok) {
                    
                    if (response.status === 200) {
                        mostrarMensajeExitoso(tipo); 
                    }
                    return response.json();
                }
                throw new Error('Network response was not ok.');
            })
            .then(data => {
                console.log(data);
            })
            .catch(error => {
                if (error.message.includes("Ya has marcado hoy.")) {
                    mostrarMensajeError(); 
                } else {
                    mostrarMensajeError(); 
                }
                console.error('There has been a problem with your fetch operation:', error);
            });
    }

    
    document.getElementById("marcar-entrada").addEventListener("click", function() {
        marcar("entrada");
        this.classList.add("selected"); 
    });

    document.getElementById("marcar-descanso").addEventListener("click", function() {
        marcar("descanso");
        this.classList.add("selected"); 
    });

    document.getElementById("marcar-regreso-descanso").addEventListener("click", function() {
        marcar("regreso_descanso");
        this.classList.add("selected");
    });

    document.getElementById("marcar-fin-turno").addEventListener("click", function() {
        marcar("fin_turno");
        this.classList.add("selected"); 
    }); 
    
});