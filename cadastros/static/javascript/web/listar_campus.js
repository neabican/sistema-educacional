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
      <a href="campus/${item.pk}" 
              style="background-image: linear-gradient(0deg, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)); position: relative;"
              class="card-campus shadow py-md-5 py-4 px-4">`

    html += `
        <div id="carousel${item.pk}" class="carousel slide" data-bs-ride="carousel"
        style="position: absolute; top: 0; right: 0; bottom: 0; left: 0; overflow: hidden; z-index: 1;">
        <div class="carousel-inner">`;

    item.fotos.forEach((foto, index) => {
        html += `
            <div class="carousel-item ${index === 0 ? 'active' : ''}">
                <img src="${foto.foto}" class="d-block w-100 h-100" alt="...">
            </div>
        `;
    });
    
    html += `
        </div>
          </div>
          <h2 class="mb-3" style="position: absolute; z-index: 2; padding: 20px;">
              ${item.instituicao.sigla} ${item.nome}
          </h2>

      <div class="info-campus" style="position: absolute; z-index: 2;">
        <span>
            <i class="bi bi-building"></i>
            <span>${item.instituicao.sigla}</span>
        </span>

        <span>
            <i class="bi bi-geo-alt-fill"></i>
            <span>${item.endereco.cidade} - ${item.endereco.estado}</span>
        </span>

        <span>
            <i class="bi bi-mortarboard-fill"></i>
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

  // Inicialize os carrosséis depois que o HTML for inserido no DOM
  campus.forEach(item => {
    const carouselElement = document.querySelector(`#carousel${item.pk}`);
    const carousel = new bootstrap.Carousel(carouselElement, {
      interval: 5000, // 5 segundos
    });
  });
}

document.addEventListener('DOMContentLoaded', (event) => {
    renderizarCards();
});

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

function limparTodosResultados() {
  pesquisa = null;
  btnLimparPesquisa.classList.add('d-none');
  inputPesquisa.value = '';

  campus = [];
  buscarCampus();
}

// Event listeners
formPesquisa.addEventListener('submit', event => {
  event.preventDefault();

  pesquisarCampus();
});

btnLimparPesquisa.addEventListener('click', limparTodosResultados);

inputPesquisa.addEventListener('keyup', () => {
 if (inputPesquisa.value.trim() === '')
  limparTodosResultados();
});

window.addEventListener('load', buscarCampus);