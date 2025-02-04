document.addEventListener('DOMContentLoaded', function () {
    const menuButton = document.getElementById('menuButton');
    const menuDropdown = document.getElementById('menuDropdown');

    menuButton.addEventListener('click', function () {
        if (menuDropdown.style.display === 'block') {
            menuDropdown.style.display = 'none';
        } else {
            menuDropdown.style.display = 'block';
        }
    });

    // Opción adicional para cerrar el menú al hacer clic fuera
    document.addEventListener('click', function (event) {
        if (!menuButton.contains(event.target) && !menuDropdown.contains(event.target)) {
            menuDropdown.style.display = 'none';
        }
    });
});
