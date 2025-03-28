const express = require('express');
const cors = require('cors');
const fs = require('fs');
const csv = require('csv-parser');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Armazenar os dados do CSV
let operadoras = [];

// Possíveis caminhos para o arquivo CSV
const possiblePaths = [
  // Caminho direto para o arquivo original
  path.join('C:', 'Users', 'katia', 'OneDrive', 'teste_nivelamento', 'BD', 'dados', 'dados_cadastrais_ANS', 'Relatorio_cadop.csv'),
  // Caminho relativo
  path.join(__dirname, '..', '..', 'BD', 'dados', 'dados_cadastrais_ANS', 'Relatorio_cadop.csv'),
  // Caminho esperado pelo código atual
  path.join(__dirname, 'data', 'Relatorio_cadop.csv')
];

// Encontrar o primeiro caminho válido
let foundPath = null;
for (const csvPath of possiblePaths) {
  console.log(`Verificando caminho: ${csvPath}`);
  if (fs.existsSync(csvPath)) {
    foundPath = csvPath;
    console.log(`✅ Arquivo encontrado em: ${csvPath}`);
    break;
  }
}

// Se não encontrou o arquivo, tente criar o diretório e sugerir para copiar o arquivo
if (!foundPath) {
  console.error('❌ ERRO: Arquivo CSV não encontrado em nenhum dos caminhos testados.');
  
  // Criar o diretório data se não existir
  const dataDir = path.join(__dirname, 'data');
  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
    console.log(`Diretório criado: ${dataDir}`);
  }
  
  // Sugerir comandos para copiar o arquivo
  console.log('\n========== COMO RESOLVER ==========');
  console.log('Execute um dos seguintes comandos para copiar o arquivo para o local correto:');
  console.log('\nOpção 1 (PowerShell):');
  console.log(`Copy-Item "C:\\Users\\katia\\OneDrive\\teste_nivelamento\\BD\\dados\\dados_cadastrais_ANS\\Relatorio_cadop.csv" -Destination "C:\\Users\\katia\\OneDrive\\teste_nivelamento\\API\\backend\\data\\"`);
  console.log('\nOpção 2 (CMD):');
  console.log(`copy "C:\\Users\\katia\\OneDrive\\teste_nivelamento\\BD\\dados\\dados_cadastrais_ANS\\Relatorio_cadop.csv" "C:\\Users\\katia\\OneDrive\\teste_nivelamento\\API\\backend\\data\\"`);
  console.log('\nDepois, execute novamente: node server.js');
  console.log('====================================');
  
  process.exit(1);
}

// Carregar o CSV
fs.createReadStream(foundPath)
  .pipe(csv({ separator: ';' }))
  .on('data', (row) => {
    // Limpar os dados
    const cleanedRow = {};
    Object.entries(row).forEach(([key, value]) => {
      cleanedRow[key] = value && typeof value === 'string' 
        ? value.replace(/^"|"$/g, '').trim() 
        : value;
    });
    operadoras.push(cleanedRow);
  })
  .on('end', () => {
    console.log(`CSV carregado: ${operadoras.length} operadoras encontradas.`);
  })
  .on('error', (error) => {
    console.error('Erro ao ler o arquivo CSV:', error);
  });

// Endpoint para busca
app.get('/api/operadoras/busca', (req, res) => {
  // Parâmetros de busca, paginação e ordenação
  const termo = req.query.termo?.toLowerCase() || '';
  const page = parseInt(req.query.page) || 1;
  const limit = parseInt(req.query.limit) || 10;
  const sortField = req.query.sort || '0'; // Usar primeira coluna se não especificado
  const sortOrder = req.query.order === 'desc' ? -1 : 1;

  // Filtrar operadoras que correspondem ao termo de busca
  const resultados = operadoras.filter(op => {
    // Buscar em todos os campos
    return Object.values(op).some(value => 
      value && typeof value === 'string' && value.toLowerCase().includes(termo)
    );
  });

  // Ordenar resultados (tratando caso especial para campos que podem não existir)
  resultados.sort((a, b) => {
    const aValue = a[sortField] || '';
    const bValue = b[sortField] || '';
    if (aValue < bValue) return -1 * sortOrder;
    if (aValue > bValue) return 1 * sortOrder;
    return 0;
  });

  // Calcular paginação
  const startIndex = (page - 1) * limit;
  const endIndex = page * limit;
  const paginatedResults = resultados.slice(startIndex, endIndex);
  
  // Preparar resposta
  const response = {
    total: resultados.length,
    totalPages: Math.ceil(resultados.length / limit),
    currentPage: page,
    limit,
    results: paginatedResults
  };

  res.json(response);
});

// Endpoint para obter todas as operadoras
app.get('/api/operadoras', (req, res) => {
  // Parâmetros de paginação e ordenação
  const page = parseInt(req.query.page) || 1;
  const limit = parseInt(req.query.limit) || 10;
  const sortField = req.query.sort || '0';
  const sortOrder = req.query.order === 'desc' ? -1 : 1;

  // Ordenar resultados
  const resultados = [...operadoras].sort((a, b) => {
    const aValue = a[sortField] || '';
    const bValue = b[sortField] || '';
    if (aValue < bValue) return -1 * sortOrder;
    if (aValue > bValue) return 1 * sortOrder;
    return 0;
  });

  // Calcular paginação
  const startIndex = (page - 1) * limit;
  const endIndex = page * limit;
  const paginatedResults = resultados.slice(startIndex, endIndex);
  
  // Preparar resposta
  const response = {
    total: operadoras.length,
    totalPages: Math.ceil(operadoras.length / limit),
    currentPage: page,
    limit,
    results: paginatedResults
  };

  res.json(response);
});

// Iniciar o servidor
app.listen(PORT, () => {
  console.log(`Servidor rodando na porta ${PORT}`);
  console.log(`Acesse http://localhost:${PORT}/api/operadoras para ver todas as operadoras`);
});