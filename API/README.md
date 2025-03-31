# 🌐 API - Operadoras ANS

Este projeto é uma aplicação para listar e buscar operadoras de saúde com base em dados fornecidos pela ANS.

---

## 📝 Descrição

O projeto é composto por:
- **Backend**: API desenvolvida em Python com Flask.
- **Frontend**: Interface desenvolvida em Vue.js.
- **Postman**: Coleção para testar os endpoints da API.

---

## ✨ Funcionalidades

- 🔍 Busca de operadoras por Razão Social, Nome Fantasia, Cidade, UF ou Modalidade.
- 📋 Listagem paginada de operadoras.
- 📊 Ordenação dos resultados por diferentes critérios.

---

## 🛠️ Pré-requisitos

- **Backend**:
  - Python 3.8+ instalado.
  - Dependências listadas no arquivo `requirements.txt`.

- **Frontend**:
  - Node.js 16+ instalado.
  - Gerenciador de pacotes `npm` ou `yarn`.

- **Postman**:
  - Postman instalado para testar os endpoints da API.

---

## 🚀 Instalação

### 1. Clone o Repositório
```bash
git clone https://github.com/Katianefatec/teste_nivelamento.git
cd teste_nivelamento
```

### 2. Configuração do Backend  

1. Navegue até o diretório do backend:
   ```bash
   cd API/backend
   ```

2. Crie um ambiente virtual e ative-o:
```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
```   

3. Instale as dependências:   
```bash
   pip install -r requirements.txt
```

4. Execute o servidor:
```bash
   python server.py
```

5. A API estará disponível em: http://localhost:3000

### 3. Configuração do Frontend  

1. Navegue até o diretório do frontend:
```bash
   cd ../frontend
```

2. Instale as dependências:
```bash
npm install
```

3. Execute o servidor de desenvolvimento:
```bash
npm run serve
```

4. Acesse o frontend em: http://localhost:8080

### 4. Teste com o Postman

1. A coleção do Postman está disponível no diretório `postman`:
   - Arquivo: `postman/API - Operadoras ANS.postman_collection.json`

2. Importe a coleção no Postman:
   - Abra o Postman.
   - Clique em **Import** no canto superior esquerdo.
   - Selecione o arquivo `postman/API - Operadoras ANS.postman_collection.json`.
   - Clique em **Import**.

3. Teste os endpoints diretamente no Postman.

---

## 🏆 Endpoints Disponíveis

### **1. Listar Operadoras**
- **URL**: `GET /api/operadoras`
- **Parâmetros de Consulta**:
  - `page`: Número da página (opcional, padrão: 1).
  - `limit`: Número de itens por página (opcional, padrão: 10).
  - `sort`: Campo para ordenação (opcional, padrão: `Razao_Social`).
  - `order`: Ordem (`asc` ou `desc`, padrão: `asc`).

### **2. Buscar Operadoras**
- **URL**: `GET /api/operadoras/busca`
- **Parâmetros de Consulta**:
  - `termo`: Termo de busca (obrigatório).
  - `page`, `limit`, `sort`, `order`: Mesmos parâmetros do endpoint anterior.

---

## ⚙️ Estrutura do Projeto

```
.
├── API/
│   ├── backend/
│   │   ├── data/
│   │   ├── routes/
│   │   ├── server.py
│   │   └── requirements.txt
│   ├── frontend/
│   │   ├── src/
│   │   ├── public/
│   │   ├── package.json
│   │   └── README.md
├── postman/
│   ├── API - Operadoras ANS.postman_collection.json
├── README.md
└── .gitignore
```

---

## 🛡️ Observações

- Certifique-se de que o backend está rodando em `http://localhost:3000` antes de iniciar o frontend.
- Use o Postman para testar os endpoints da API.
- Para personalizar a API, edite os arquivos no diretório `API/backend`.

