<template>
  <div class="card mb-4">
    <div class="card-body">
      <div class="row g-3">
        <!-- Campo de busca -->
        <div class="col-md-8">
          <div class="input-group">
            <input 
              type="text" 
              class="form-control" 
              placeholder="Digite sua busca..." 
              :value="termoBusca"
              @input="$emit('update:termoBusca', $event.target.value)"
              @keyup.enter="buscar"
            />
            <button 
              class="btn btn-primary" 
              type="button"
              @click="buscar"
            >
              Buscar
            </button>
          </div>
          <small class="form-text text-muted">
            Busca por Razão Social, Nome Fantasia, Cidade, UF ou Modalidade
          </small>
        </div>
        
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    termoBusca: {
      type: String,
      required: true
    },
    ordenacao: {
      type: String,
      required: true
    }
  },
  methods: {
    buscar() {
      this.$emit('buscar');
    }
  }
};
</script>

<style scoped>
/* Estilos específicos para o componente */
.input-group {
  display: flex;
  align-items: center;
}
.form-text {
  font-size: 0.9rem;
  color: #6c757d;
}
</style>