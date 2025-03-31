# 📊 Banco de Dados da ANS

**Scripts SQL para criação, importação e consultas no banco de dados da ANS**

## 📝 Descrição

Este repositório contém scripts SQL para:
- Criação das tabelas do banco de dados
- Importação de dados cadastrais e demonstrações contábeis
- Consultas para análise de dados, como as 10 operadoras com maior despesa no último trimestre

Nota: Você pode executar os scripts diretamente no **PowerShell** ou no **Prompt de Comando (cmd)**.

---

## ✨ Funcionalidades

- 🛠️ Criação automática das tabelas no banco de dados
- 📥 Importação de dados a partir de arquivos CSV
- 🔍 Consultas SQL para análise de dados
- 📊 Relatórios de despesas e desempenho das operadoras

---

## 🛠️ Pré-requisitos

- MySQL 8.0+ instalado
- Banco de dados `ans_db` criado no MySQL
- Arquivos CSV disponíveis no diretório `BD/dados`
- **PowerShell** ou **Prompt de Comando (cmd)** instalado no sistema

---

## 🚀 Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/Katianefatec/teste_nivelamento.git
   cd BD
   ```

2. Configure o MySQL para permitir a importação de arquivos locais:
   ```sql
   SET GLOBAL local_infile = 1;
   ```

3. Certifique-se de que o usuário MySQL tem permissão para `LOAD DATA INFILE`.

4. É necessário ter gerado o arquivo Relatorio_cadop.csv, presente no diretório WebScraping.

---

## 🏆 Como Usar

### 1. Criação das Tabelas

#### No **Prompt de Comando (cmd)**:
Execute o script com:
```cmd
net start MySQL
mysql -u root -p -e "CREATE DATABASE ans_db;"
mysql -u root -p ans_db < scripts\criar_tabelas.sql
```

#### No **PowerShell**:
Use o comando `Get-Content` para redirecionar o conteúdo do arquivo:
```powershell
Start-Service MySQL
mysql -u root -p -e "CREATE DATABASE ans_db;"
Get-Content .\scripts\criar_tabelas.sql | mysql -u root -p ans_db
```

---

### 2. Importação de Dados

#### No **Prompt de Comando (cmd)**:

Execute o script com:
```cmd
cd BD/scripts
mysql --local-infile=1 -u root -p ans_db < importar_dados.sql
```

#### No **PowerShell**:
Use o comando `Get-Content`:
```powershell
Get-Content .\scripts\importar_dados.sql | mysql -u root -p ans_db
```

### 3. Consultas

#### No **Prompt de Comando (cmd)**:
Execute as consultas com:
```cmd
cd BD/consultas
mysql -u root -p ans_db < consultas\10OpMaiorDesp4T.sql
```

#### No **PowerShell**:
Use o comando `Get-Content`:
```powershell
Get-Content .\consultas\10OpMaiorDesp4T.sql | mysql -u root -p ans_db
```

---

### 4. Consultas Automatizadas com PowerShell

Você também pode usar o script `executar_consultas.ps1` para executar várias consultas automaticamente.

#### Passos:
1. Abra o **PowerShell**.
2. Navegue até o diretório `BD/consultas`:
   ```powershell
   cd BD/consultas
   ```

3. Execute o script passando a senha do MySQL como parâmetro:
   ```powershell
   .\executar_consultas.ps1 -senhaMySQL "sua_senha"
   ```

---

## ⚙️ Estrutura do Projeto

```
.
├── consultas/               # Consultas SQL
│   ├── 10OpMaiorDesp4T.sql  # 10 operadoras com maior despesa no 4º trimestre
│   ├── 10OpMaiorDespUltimoAno.sql # 10 operadoras com maior despesa no último ano
│   ├── executar_consultas.ps1 # Script PowerShell para executar consultas
├── dados/                   # Arquivos CSV para importação
│   ├── dados_cadastrais_ANS/
│   │   └── Relatorio_cadop.csv
│   ├── dem_contabeis_2023_2024/
│   │   ├── 1T2023.csv
│   │   ├── 2T2023.csv
│   │   ├── 3T2023.csv
│   │   ├── 4T2023.csv
│   │   ├── 1T2024.csv
│   │   ├── 2T2024.csv
│   │   ├── 3T2024.csv
│   │   └── 4T2024.csv
├── scripts/                 # Scripts SQL para criação e importação
│   ├── criar_tabelas.sql    # Criação das tabelas
│   ├── importar_dados.sql   # Importação de dados
└── README.md                # Este arquivo
```

---

## 🛡️ Observações

- Certifique-se de que o MySQL está configurado para permitir a importação de arquivos locais (`LOAD DATA INFILE`).
- Os arquivos CSV devem estar no formato esperado, com separador `;` e codificação UTF-8.
- Use o **Prompt de Comando (cmd)** ou o **PowerShell** com os comandos adequados para executar os scripts.

