'use strict';

function abrirModalInformacoes(nome, id, vagas) {
  document.getElementById('nome-curso').textContent = nome;

  const descricao = document.getElementById(`descricao-${id}`).innerText;
  document.getElementById('descricao-curso').innerHTML = descricao;
}