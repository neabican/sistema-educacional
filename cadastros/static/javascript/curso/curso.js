'use strict';

function abrirModalInformacoes(nome, id, vagas) {
  document.getElementById('nome-curso').textContent = nome;
  document.getElementById('vagas-curso').textContent = vagas;

  const descricao = document.getElementById(`descricao-${id}`).innerText;
  document.getElementById('descricao-curso').innerHTML = descricao;
}