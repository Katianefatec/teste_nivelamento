import pdfplumber
import pandas as pd
import zipfile
import os

def extrair_dados_pdf(caminho_pdf):
    """Extrai dados do PDF e retorna uma lista de dicionários"""
    dados = []

    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            linhas = texto.split('\n')

            for linha in linhas:
                if "OD" in linha or "AMB" in linha:
                    partes = linha.split()
                    dados.append({
                        "Procedimento": " ".join(partes[:-2]),
                        "OD": partes[-2],
                        "AMB": partes[-1]
                    })

    return dados

def salvar_csv(dados, caminho_csv):
    """Salva os dados extraídos em um arquivo CSV"""
    df = pd.DataFrame(dados)
    df['OD'] = df['OD'].replace({'OD': 'Descrição Completa OD'})
    df['AMB'] = df['AMB'].replace({'AMB': 'Descrição Completa AMB'})
    
    # Cria o diretório se não existir
    os.makedirs(os.path.dirname(caminho_csv), exist_ok=True)
    
    df.to_csv(caminho_csv, index=False)

def descompactar_zip(caminho_zip, extrair_para):
    """Descompacta o arquivo ZIP"""
    with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
        zip_ref.extractall(extrair_para)

def compactar_arquivo(caminho_arquivo, caminho_zip):
    """Compacta o arquivo em um arquivo ZIP"""
    with zipfile.ZipFile(caminho_zip, 'w') as zipf:
        zipf.write(caminho_arquivo, os.path.basename(caminho_arquivo))

def main():
    caminho_zip = "data/Anexos_ANS.zip"
    extrair_para = "data"
    caminho_pdf = os.path.join(extrair_para, "Anexo_I.pdf")
    caminho_csv = "data/Anexo_I.csv"
    caminho_zip_final = "Teste_Katiane.zip"

    # Descompacta o arquivo ZIP
    descompactar_zip(caminho_zip, extrair_para)

    # Verifica se o arquivo PDF foi extraído corretamente
    if not os.path.exists(caminho_pdf):
        print(f"Erro: O arquivo {caminho_pdf} não foi encontrado após a extração.")
        return

    # Extrai dados do PDF e salva em CSV
    dados = extrair_dados_pdf(caminho_pdf)
    salvar_csv(dados, caminho_csv)
    print(f"Dados extraídos e salvos em {caminho_csv}")

    # Compacta o arquivo CSV em um arquivo ZIP final
    compactar_arquivo(caminho_csv, caminho_zip_final)
    print(f"Arquivo CSV compactado em {caminho_zip_final}")

    # Remove arquivos temporários
    os.remove(caminho_pdf)
    os.remove(caminho_csv)

if __name__ == "__main__":
    main()