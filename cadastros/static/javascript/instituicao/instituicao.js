'use stritct';

function abrirModalEdicao(nome, pk) {
  document.getElementById('nome-edicao').value = nome;
  document.getElementById('pk-edicao').value = pk;
}

function abrirModalDelecao(pk) {
  document.getElementById('pk-delecao').value = pk;
}