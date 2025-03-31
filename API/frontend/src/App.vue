<template>
  <div id="app" class="container mt-4">
    <h1 class="mb-4">Busca de Operadoras ANS</h1>
    
    <FormBusca 
      v-model:termoBusca="termoBusca" 
      v-model:ordenacao="ordenacao" 
      @buscar="buscarOperadoras" 
    />
    
    <div v-if="carregando" class="loading-overlay">      
      <p class="mt-3">Buscando operadoras...</p>
    </div>
    
    <div v-else-if="erro" class="alert alert-danger mt-3">
      {{ erro }}
    </div>
    
    <TabelaResultados 
      v-else-if="resultados && resultados.length" 
      :resultados="resultados" 
      :total="total" 
      :paginaAtual="paginaAtual" 
      :totalPaginas="totalPaginas" 
    />
    
    <div v-else-if="buscaRealizada" class="alert alert-info mt-3">
      <p class="text-center">Nenhuma operadora encontrada.</p>
    </div>
    
    <PaginacaoOperadoras
      v-if="!carregando && totalPaginas > 1" 
      :paginaAtual="paginaAtual" 
      :totalPaginas="totalPaginas" 
      :paginas="paginas" 
      @mudar-pagina="mudarPagina" 
    />
  </div>
</template>

<script>
import FormBusca from './components/FormBusca.vue';
import TabelaResultados from './components/TabelaResultados.vue';
import PaginacaoOperadoras from './components/PaginacaoOperadoras.vue';
import axios from 'axios';

export default {
  components: {
    FormBusca,
    TabelaResultados,
    PaginacaoOperadoras
  },
  data() {
    return {
      termoBusca: '',
      resultados: [],
      total: 0,
      paginaAtual: 1,
      totalPaginas: 0,
      itensPorPagina: 10,
      ordenacao: 'Razao_Social|asc',
      carregando: false,
      buscaRealizada: false,
      erro: null,
      apiUrl: 'http://localhost:3000/api'
    };
  },
  computed: {
    paginas() {
      const pages = [];
      const maxPagesToShow = 5;
      
      let startPage = Math.max(1, this.paginaAtual - Math.floor(maxPagesToShow / 2));
      let endPage = Math.min(this.totalPaginas, startPage + maxPagesToShow - 1);
      
      if (endPage - startPage + 1 < maxPagesToShow) {
        startPage = Math.max(1, endPage - maxPagesToShow + 1);
      }
      
      for (let i = startPage; i <= endPage; i++) {
        pages.push(i);
      }
      
      return pages;
    }
  },
  mounted() {
    // Carregar operadoras quando o componente for montado
    this.buscarOperadoras();
  },
  methods: {
    async buscarOperadoras() {
  this.carregando = true;
  this.buscaRealizada = true;
  this.erro = null;

  try {
    const [campo, ordem] = this.ordenacao.split('|');
    const endpoint = this.termoBusca 
      ? `${this.apiUrl}/operadoras/busca`
      : `${this.apiUrl}/operadoras`;

    console.log('Fazendo requisição para:', endpoint, {
      params: {
        termo: this.termoBusca,
        page: this.paginaAtual,
        limit: this.itensPorPagina,
        sort: campo,
        order: ordem
      }
    });
    
    const response = await axios.get(endpoint, {
      params: {
        termo: this.termoBusca,
        page: this.paginaAtual,
        limit: this.itensPorPagina,
        sort: campo,
        order: ordem
      }
    });

    console.log('Resposta bruta:', response);
    console.log('Resposta data:', response.data);
    console.log('Resposta results:', response.data.results);
    
    // Garantir que resultados seja um array
    if (!response.data.results) {
      console.error('Não foram encontrados resultados na resposta');
      this.resultados = [];
    } else {
      this.resultados = response.data.results;
      console.log('Resultados atribuídos:', this.resultados);
    }
    
    this.total = response.data.total || 0;
    this.totalPaginas = response.data.totalPages || 0;
    this.paginaAtual = response.data.currentPage || 1;
  } catch (error) {
    console.error('Erro detalhado:', error.response || error);
    this.erro = 'Erro ao buscar operadoras. Por favor, tente novamente.';
    this.resultados = [];
  } finally {
    this.carregando = false;
  }
},
    mudarPagina(pagina) {
      if (pagina !== this.paginaAtual) {
        this.paginaAtual = pagina;
        this.buscarOperadoras();
      }
    }
  }
};
</script>

