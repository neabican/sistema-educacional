'use stritct';

function abrirModalEdicao(nome, sigla, pk) {
  document.getElementById('nome-edicao').value = nome;
  document.getElementById('sigla-edicao').value = sigla;
  document.getElementById('pk-edicao').value = pk;
}