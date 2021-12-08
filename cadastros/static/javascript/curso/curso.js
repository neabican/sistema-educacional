'use strict';

function abrirModalInformacoes(nome, descricao) {
  document.getElementById('nome-curso').textContent = nome;
  document.getElementById('descricao-curso').textContent = descricao;
}

function abrirModalDelecao(pk) {
  document.getElementById('pk-delecao').value = pk;
}