function toggleMenu(postId) {
    var menu = document.getElementById("menu" + postId);
    menu.classList.toggle("show");
}

document.getElementById('custom-upload-button').addEventListener('click', function() {
    document.querySelector('.custom-file-input').click();
});

// Escuchar cambios en el campo de entrada de archivos
document.querySelector('#id_image').addEventListener('change', function() {
    // Obtener el contenedor de vista previa de imágenes
    var previewContainer = document.querySelector('#selected-images-preview');
    // Limpiar el contenedor de vista previa
    previewContainer.innerHTML = '';

    // Recorrer los archivos seleccionados
    for (var i = 0; i < this.files.length; i++) {
        var file = this.files[i];
        
        // Crear un elemento de imagen para la vista previa
        var img = document.createElement('img');
        img.src = URL.createObjectURL(file);
        img.alt = 'Imagen adjunta';

        // Agregar la imagen al contenedor de vista previa
        previewContainer.appendChild(img);
    }
});

window.onclick = function(event) {
    if (!event.target.matches('.menu a')) {
        var menus = document.getElementsByClassName('dropdown-content');
        for (var i = 0; i < menus.length; i++) {
            var menu = menus[i];
            if (menu.classList.contains('show')) {
                menu.classList.remove('show');
            }
        }
    }
}

$(document).ready(function() {
    $(document).on("submit", ".like-form", function(e) {
        e.preventDefault();

        var form = $(this);
        var likeButton = form.find(".like-button");
        $.ajax({
            type: "POST",
            url: form.attr("action"),
            data: form.serialize(),
            dataType: "json",
            success: function(data) {
                var likeImage = data.is_like ?'{% static 'img/left-bar/dislike.png' %}':'{% static 'img/left-bar/like.png' %}' ;
                likeButton.find('img').attr('src', likeImage);
                form.siblings(".likes-count").text(data.likes_count);
            }
        });
    });
});
document.querySelectorAll('.abrirModalComment').forEach(function(button) {
    button.addEventListener('click', function() {
        const modalId = this.getAttribute('data-modal-target');
        const modal = document.getElementById(modalId);
        modal.style.display = 'block';
    });
});

// Agrega un controlador de eventos para cerrar el modal cuando se hace clic en "Cerrar"
document.querySelectorAll('.closeComment').forEach(function(closeButton) {
    closeButton.addEventListener('click', function() {
        const modal = this.closest('.modal-comment');
        modal.style.display = 'none';
    });
});

// ajax para los comentarios 
$(document).ready(function() {
    $(".comment-submit").on("click", function(event) {
        event.preventDefault(); // Evitar que se envíe el formulario automáticamente

        var form = $(this).closest("form");
        var formData = new FormData(form[0]);

        $.ajax({
            type: form.attr("method"),
            url: form.attr("action"),
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                if (data.success) {
                    // Comentario guardado con éxito, realiza acciones necesarias
                    alert(data.message); // Muestra un mensaje de éxito (puedes personalizar esto)
                    // Puedes recargar la página o realizar otras acciones necesarias aquí
                } else {
                    alert(data.message); // Muestra un mensaje de error
                }
            }
        });
    });
});