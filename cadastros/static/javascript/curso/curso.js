'use strict';

function abrirModalInformacoes(nome, descricao) {
  document.getElementById('nome-curso').textContent = nome;
  document.getElementById('descricao-curso').innerHTML = descricao;
}