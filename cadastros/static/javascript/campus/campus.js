'use strict';

const coordenadas = JSON.parse(document.getElementById('coordenadas').textContent);
const map = L.map('map').setView([coordenadas.latitude, coordenadas.longitude], 15);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
  attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
  maxZoom: 18,
  id: 'mapbox/streets-v11',
  tileSize: 512,
  zoomOffset: -1,
  accessToken: 'pk.eyJ1IjoieHVuaXRvIiwiYSI6ImNrd3d2c2Z4NjA3NjczNHF0b2JwcnZ5OXMifQ.6u3NKOX3gQlF1Yo1_7L12g'
}).addTo(map);

L.marker([coordenadas.latitude, coordenadas.longitude]).addTo(map);

function abrirModalInformacoes(nome, descricao, link) {
  document.getElementById('info-nome').textContent = nome;
  document.getElementById('info-descricao').innerHTML = descricao;

  console.log(descricao);

  if (link.trim() != 'None') {
    document.getElementById('info-link-wrapper').classList.remove('d-none');
    document.getElementById('info-link').href = link;
  } else {
    document.getElementById('info-link-wrapper').classList.add('d-none');
    document.getElementById('info-link').href = '#';
  }
}

function abrirModalDelecao(event, tipo) {
  // Buscando a URL para a deleção do registro através do ID
  const url = event.target.id ? event.target.id : event.target.parentNode.id;
  
  document.getElementById('button-submit').href = url;
  document.getElementById('modal-delecao-label').textContent = `Deletar ${tipo}`;
}