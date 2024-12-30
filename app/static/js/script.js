function toggleIlustracaoField() {
    const ilustracaoField = document.getElementById('ilustracaoField');
    ilustracaoField.style.display = document.getElementById('ilustracaoCheckbox').checked ? 'block' : 'none';
    document.getElementById('ilustracao').value = 0
}

function toggleTabelaField() {
    const tabelaField = document.getElementById('tabelaField');
    tabelaField.style.display = document.getElementById('tabelaCheckbox').checked ? 'block' : 'none';
    document.getElementById('tabela').value = 0
}

function confirmarAcao(acao, url) {
    if (confirm(`Você tem certeza que deseja ${acao} este pedido?`)) {
        const form = document.getElementById('confirmForm');
        form.action = url; 
        const inputAcao = document.createElement('input');
        inputAcao.type = 'hidden';
        inputAcao.name = 'acao';
        inputAcao.value = acao;
        form.appendChild(inputAcao);

        console.log(`Ação: ${acao}, URL: ${url}`); 
        form.submit()
    }
}

document.getElementById('statusFilter').addEventListener('change', function() {
    const selectedStatus = this.value;
    const pedidoItems = document.querySelectorAll('.pedido-item');

    pedidoItems.forEach(item => {
        const pedidoStatus = item.getAttribute('data-status');
        if (selectedStatus === 'todos' || pedidoStatus === selectedStatus) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
});
