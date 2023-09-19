document.addEventListener("DOMContentLoaded", function () {
	const formularioRegistro = document.getElementById("miFormulario");
	const formularioLogin = document.getElementById("formulario");
  
	if (formularioRegistro) {
	  formularioRegistro.addEventListener("submit", validarRegistro);
	}
  
	if (formularioLogin) {
	  formularioLogin.addEventListener("submit", validarLogin);
	}
  
	function validarNombre(nombre) {
	  return /^[a-zA-Z\s]{2,50}$/.test(nombre);
	}
  
	function validarCorreo(correo) {
	  return /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/.test(correo);
	}
  
	function validarContrasena(contrasena) {
	  // La contraseña debe tener al menos 8 caracteres, una letra mayúscula, una letra minúscula y un número.
	  return /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/.test(contrasena);
	}
  
	function mostrarError(input, mensaje) {
	  const grupo = input.parentElement;
	  const mensajeError = grupo.querySelector(".formulario__input-error");
	  mensajeError.textContent = mensaje;
	  grupo.classList.add("formulario__grupo-incorrecto");
	}
  
	function quitarError(input) {
	  const grupo = input.parentElement;
	  grupo.classList.remove("formulario__grupo-incorrecto");
	}
  
	function validarRegistro(event) {
	  event.preventDefault();
	  const nombre = document.getElementById("Clie_Nombre");
	  const correo = document.getElementById("Usua_Correo");
	  const contrasena = document.getElementById("Usua_Pass");
	  const confirmarContrasena = document.getElementById("confirm_Pass");
	  const aceptarTerminos = document.getElementById("terminos");
  
	  if (!validarNombre(nombre.value)) {
		mostrarError(nombre, "El nombre debe contener solo letras y espacios (2-50 caracteres).");
	  } else {
		quitarError(nombre);
	  }
  
	  if (!validarCorreo(correo.value)) {
		mostrarError(correo, "El correo electrónico no es válido.");
	  } else {
		quitarError(correo);
	  }
  
	  if (!validarContrasena(contrasena.value)) {
		mostrarError(contrasena, "La contraseña debe tener al menos 8 caracteres, una letra mayúscula, una letra minúscula y un número.");
	  } else {
		quitarError(contrasena);
	  }
  
	  if (contrasena.value !== confirmarContrasena.value) {
		mostrarError(confirmarContrasena, "Las contraseñas no coinciden.");
	  } else {
		quitarError(confirmarContrasena);
	  }
  
	  if (!aceptarTerminos.checked) {
		mostrarError(aceptarTerminos.parentElement, "Debes aceptar los términos y condiciones.");
	  } else {
		quitarError(aceptarTerminos.parentElement);
	  }
	}
  
	function validarLogin(event) {
	  event.preventDefault();
	  const correo = document.getElementById("correo");
	  const contrasena = document.getElementById("password");
  
	  if (!validarCorreo(correo.value)) {
		mostrarError(correo, "El correo electrónico no es válido.");
	  } else {
		quitarError(correo);
	  }
  
	  if (!validarContrasena(contrasena.value)) {
		mostrarError(contrasena, "La contraseña debe tener al menos 8 caracteres, una letra mayúscula, una letra minúscula y un número.");
	  } else {
		quitarError(contrasena);
	  }
	}
  });
  