// static/js/script.js
console.log("Posto Django em funcionamento!");

// Exemplo de JS para um botão na home
document.addEventListener('DOMContentLoaded', (event) => {
    const btnServicos = document.querySelector('.btn-danger');
    if (btnServicos) {
        btnServicos.addEventListener('click', () => {
            alert("Aguarde, estamos te redirecionando para os serviços!");
        });
    }
});