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
git clone https://github.com/seu-usuario/download-anexos-ans.git
cd download-anexos-ans

# Instale as dependências
pip install -r requirements.txt
```

## 🏆 Como Usar

Execute o script com:

```bash
python download_anexos.py
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

## ⚙️ Estrutura do Projeto

```
.
├── baixa_pdf.py     # Script principal
├── README.md             # Este arquivo
├── requirements.txt      # Dependências
└── .gitignore           # Arquivos ignorados
```
