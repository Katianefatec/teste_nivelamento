<template>
  <div>
       
    <div v-if="resultados && resultados.length > 0" class="card">
      <div class="card-header bg-light d-flex justify-content-between align-items-center">
        <span><strong>{{ total }}</strong> operadoras encontradas</span>
        <span>Página {{ paginaAtual }} de {{ totalPaginas }}</span>
      </div>
      
      <div class="table-container">
        <table class="table table-hover mb-0">
          <thead>
            <tr>
              <th>Registro ANS</th>
              <th>Razão Social</th>
              <th>Nome Fantasia</th>
              <th>Modalidade</th>
              <th>Cidade</th>
              <th>UF</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(op, index) in resultados" :key="index">
              <td>{{ op.Registro_ANS }}</td>
              <td>{{ op.Razao_Social }}</td>
              <td>{{ op.Nome_Fantasia || '-' }}</td>
              <td>{{ op.Modalidade }}</td>
              <td>{{ op.Cidade }}</td>
              <td>{{ op.UF }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div v-else class="alert alert-info mt-3">
      <p class="text-center mb-0">Nenhuma operadora encontrada.</p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    resultados: {
      type: Array,
      required: false,
      default: () => [] 
    },
    total: {
      type: Number,
      required: false,
      default: 0
    },
    paginaAtual: {
      type: Number,
      required: false,
      default: 1
    },
    totalPaginas: {
      type: Number,
      required: false,
      default: 1
    }
  },
  mounted() {
    console.log('TabelaResultados montado:', this.resultados);
  },
  updated() {
    console.log('TabelaResultados atualizado:', this.resultados);
  }
};
</script>