'use strict';

const formPesquisa = document.getElementById('form-pesquisa');
const inputPesquisa = document.getElementById('input-pesquisa');
const btnLimparPesquisa = document.getElementById('btn-limpar-pesquisa');

const listaCampus = document.getElementById('lista-campus');

let campus = [];
let pesquisa = null;
let pagAtual = 0;

var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));

var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
});

function renderizarCards() {
  let html = '';

  campus.forEach(item => {
    html += `
      <a 
        href="campus/${item.pk}" 
        style="background-image: linear-gradient(0deg, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('${item.foto}');"
        class="card-campus shadow py-md-5 py-4 px-4"
      >
        <h2 class="mb-3">${item.nome}</h2>

        <div class="info-campus">
          <span>
            <i class="fa fa-map-marker-alt"></i>
            <span>${item.endereco.cidade} - ${item.endereco.estado}</span>
          </span>

          <span>
            <i class="fa fa-graduation-cap"></i>
            <span>${item.cursos.length} Cursos Ofertados</span>
          </span>
        </div>
      </a>
    `;
  });

  html += `
    <button id="btn-carregar-resultados" onclick="carregarMaisResultados()">
      Carregar mais resultados
    </button>
  `;

  listaCampus.innerHTML = html;
}

async function pesquisarCampus() {
  const nomeCampus = inputPesquisa.value;

  if (nomeCampus.trim() === '')
    return;

  campus = [];
  pesquisa = nomeCampus.trim();

  const response = await fetch(`/api/campus?pag=${0}&campus=${pesquisa}`, {
    method: 'GET',
  });

  const dados = await response.json(response.data);
  dados.forEach(item => campus.push(item));

  btnLimparPesquisa.classList.remove('d-none');

  renderizarCards();
}

async function buscarCampus() {
  const novaPag = Math.floor(campus.length / 10);

  if (pagAtual === novaPag && campus.length > 0)
    return document.getElementById('btn-carregar-resultados').classList.add('d-none');

  pagAtual = novaPag;

  const url = pesquisa ? `/api/campus?pag=${pagAtual}&campus=${pesquisa}` : `/api/campus?pag=${pagAtual}`;

  const response = await fetch(url, {
    method: 'GET',
  });

  const dados = await response.json(response.data);

  if (dados.length === 0)
    return document.getElementById('btn-carregar-resultados').classList.add('d-none');

  dados.forEach(item => campus.push(item));

  renderizarCards();
}

function carregarMaisResultados() {
  document.getElementById('btn-carregar-resultados').innerHTML = '<i class="fas fa-spinner spin"></i>';
  buscarCampus();
}

// Event listeners
formPesquisa.addEventListener('submit', event => {
  event.preventDefault();

  pesquisarCampus();
});

btnLimparPesquisa.addEventListener('click', () => {
  pesquisa = null;
  btnLimparPesquisa.classList.add('d-none');
  inputPesquisa.value = '';
  
  campus = [];
  buscarCampus();
});

window.addEventListener('load', buscarCampus);