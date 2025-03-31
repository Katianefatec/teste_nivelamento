<template>
  <nav class="pagination-container">
    <ul class="pagination">
      <li
        class="page-item"
        :class="{ disabled: paginaAtual === 1 }"
        @click="mudarPagina(paginaAtual - 1)"
      >
        <span class="page-link">Anterior</span>
      </li>
      <li
        v-for="pagina in paginas"
        :key="pagina"
        class="page-item"
        :class="{ active: pagina === paginaAtual }"
        @click="mudarPagina(pagina)"
      >
        <span class="page-link">{{ pagina }}</span>
      </li>
      <li
        class="page-item"
        :class="{ disabled: paginaAtual === totalPaginas }"
        @click="mudarPagina(paginaAtual + 1)"
      >
        <span class="page-link">Próximo</span>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  props: {
    paginaAtual: {
      type: Number,
      required: true,
    },
    totalPaginas: {
      type: Number,
      required: true,
    },
    paginas: {
      type: Array,
      required: true,
    },
  },
  methods: {
    mudarPagina(pagina) {
      if (pagina > 0 && pagina <= this.totalPaginas) {
        this.$emit('mudar-pagina', pagina);
      }
    },
  },
};
</script>

