function copiarPassword(id) {
    fetch(`/accounts/${id}`)
        .then(response => response.json())
        .then(data => {
            navigator.clipboard.writeText(data.password)
                .then(() => {
                    Swal.fire({
                        title: 'Copiado',
                        text: 'La contraseña fue copiada al portapapeles',
                        icon: 'success',
                        timer: 2000,
                        showConfirmButton: false
                    });
                })
                .catch(err => {
                    Swal.fire('Error', 'No se pudo copiar la contraseña', 'error');
                });
        });
}