/*
 * static/js/script.js
 *
 * Arquivo JavaScript global do projeto. Contém exemplos simples de comportamento
 * interativo usado nas páginas. Em projetos maiores recomendamos modularizar o
 * código (ex.: um arquivo por componente ou usar bundlers). Mantivemos código
 * leve e compatível com navegadores modernos sem dependências adicionais.
 */

// Mensagem no console para indicar que o JS da aplicação está carregado.
console.log("Posto Django em funcionamento!");

// Exemplo simples: quando o DOM estiver carregado, procura por um botão específico
// e adiciona um listener. Observações:
//  - Usar seletores mais específicos é uma boa prática para evitar conflitos
//  - Em produção, prefira delegação de eventos ou frameworks se houver UI rica
document.addEventListener('DOMContentLoaded', () => {
    // Busca um botão com a classe .btn-danger, que no template atual é usado
    // para o botão 'Sair' no cabeçalho. Aqui usamos com fins ilustrativos.
    const btnServicos = document.querySelector('.btn-danger');
    if (btnServicos) {
        btnServicos.addEventListener('click', () => {
            // Exibe uma mensagem simples. Em aplicações reais, evite alerts para
            // não interromper a experiência do usuário; prefira modais custom.
            alert("Aguarde, estamos te redirecionando para os serviços!");
        });
    }
});