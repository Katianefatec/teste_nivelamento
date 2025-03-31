<template>
  <nav aria-label="Navegação de páginas">
    <ul class="pagination">
      <li class="page-item" :class="{ disabled: paginaAtual <= 1 }">
        <a class="page-link" href="#" @click.prevent="mudarPagina(paginaAtual - 1)">Anterior</a>
      </li>
      
      <li 
        v-for="pagina in paginas" 
        :key="pagina"
        class="page-item" 
        :class="{ active: pagina === paginaAtual }"
      >
        <a class="page-link" href="#" @click.prevent="mudarPagina(pagina)">
          {{ pagina }}
        </a>
      </li>
      
      <li class="page-item" :class="{ disabled: paginaAtual >= totalPaginas }">
        <a class="page-link" href="#" @click.prevent="mudarPagina(paginaAtual + 1)">Próximo</a>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  props: ['paginaAtual', 'totalPaginas', 'paginas'],
  methods: {
    mudarPagina(pagina) {
      this.$emit('mudar-pagina', pagina);
    }
  }
};
</script>