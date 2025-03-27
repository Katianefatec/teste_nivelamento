# 📂 Download de Anexos da ANS

**Script Python para download automático dos Anexos I e II do Rol de Procedimentos da ANS**

## 📝 Descrição

Este repositório contém um script Python que automatiza o download dos:
- Anexo I (Lista de Procedimentos)
- Anexo II (Diretrizes de Utilização)

Disponíveis no portal da [Agência Nacional de Saúde Suplementar](https://www.gov.br/ans).

## ✨ Funcionalidades

- ⚡ Download automático dos PDFs mais recentes
- 📦 Compactação em arquivo ZIP único
- ✔️ Verificação de integridade dos downloads
- 📊 Relatório de tamanho dos arquivos

## 🛠️ Pré-requisitos

- Python 3.6+
- Bibliotecas listadas em `requirements.txt`

## 🚀 Instalação

```bash
# Clone o repositório
git clone https://github.com/Katianefatec/teste_nivelamento.git
cd WebScraping

# Instale as dependências
pip install -r requirements.txt
```

## 🏆 Como Usar

Download dos PDFS

Execute o script com:

```bash
python baixa_pdf.py
```

Saída esperada:
```
Acessando https://www.gov.br/ans/...
Baixando Anexo_I.pdf...
Anexo_I.pdf baixado (1452.3 KB)
Baixando Anexo_II.pdf...
Anexo_II.pdf baixado (980.5 KB)

Arquivos compactados em Anexos_ANS.zip
```
Extração de Dados para CSV
Depois de baixar os PDFs, extraia os dados do Anexo I para CSV:

```bash
python extrai_dados.py
```

Saída esperada:
```
Legenda encontrada: {'OD': 'Seg. Odontológica', 'AMB': 'Seg. Ambulatorial', ...}
Extraídos 3500 registros
CSV salvo em data/Anexo_I.csv
Arquivo compactado em data/Teste_Katiane.zip
```

## ⚙️ Estrutura do Projeto

```
.
├── baixa_pdf.py         # Script para download dos PDFs
├── extrai_dados.py      # Script para extração de dados para CSV
├── README.md            # Este arquivo
├── requirements.txt     # Dependências
├── .gitignore           # Arquivos ignorados
└── data/                # Diretório para armazenar arquivos
    ├── Anexos_ANS.zip   # PDFs compactados
    ├── Anexo_I.csv      # Dados extraídos em formato CSV
    └── Teste_Katiane.zip # Arquivo CSV compactado
```
> **Nota:** O diretório data não aparece no repositório, pois está no .gitignore