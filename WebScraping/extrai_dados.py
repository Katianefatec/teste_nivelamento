import pdfplumber
import pandas as pd
import zipfile
import os

def extrair_legenda_do_pdf(pdf_path):
    """Extrai a legenda do rodapé do PDF"""
    with pdfplumber.open(pdf_path) as pdf:
        ultima_pagina = pdf.pages[-1]
        texto_rodape = ultima_pagina.extract_text() or ""
        
        legenda = {}
        for linha in texto_rodape.split('\n'):
            linha = linha.strip()
            if ':' in linha:
                sigla, descricao = linha.split(':', 1)
                legenda[sigla.strip()] = descricao.strip()
        
        return legenda

def descompactar_zip(caminho_zip, extrair_para, arquivo_necessario):
    """Descompacta apenas o arquivo necessário do ZIP"""
    with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file == arquivo_necessario:
                zip_ref.extract(file, extrair_para)

def extrair_dados_pdf(caminho_pdf):
    """Extrai dados do PDF e retorna uma lista de dicionários"""
    dados = []
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            linhas = texto.split('\n')
            for linha in linhas:
                partes = linha.split()
                if len(partes) >= 9 and any(sigla in linha for sigla in ["OD", "AMB", "HCO", "HSO", "REF", "PAC", "DUT"]):
                    dados.append({
                        "Procedimento": " ".join(partes[:-8]),
                        "RN": partes[-8],
                        "Vigência": partes[-7],
                        "OD": partes[-6],
                        "AMB": partes[-5],
                        "HCO": partes[-4],
                        "HSO": partes[-3],
                        "REF": partes[-2],
                        "PAC": partes[-1]
                    })
    return dados

def substituir_siglas_por_descricao(df, legenda):
    """Substitui as siglas pelas descrições completas no DataFrame"""
    for coluna in df.columns:
        df[coluna] = df[coluna].apply(lambda x: legenda.get(x, x))
    return df

def salvar_csv(dados, caminho_csv, legenda):
    """Salva os dados extraídos em um arquivo CSV"""
    df = pd.DataFrame(dados)
    df = substituir_siglas_por_descricao(df, legenda)
    
    os.makedirs(os.path.dirname(caminho_csv), exist_ok=True)
    df.to_csv(caminho_csv, index=False, sep=',')

def compactar_arquivo(caminho_arquivo, caminho_zip):
    """Compacta o arquivo em um arquivo ZIP"""
    with zipfile.ZipFile(caminho_zip, 'w') as zipf:
        zipf.write(caminho_arquivo, os.path.basename(caminho_arquivo))

def main():
    caminho_zip = "data/Anexos_ANS.zip"
    extrair_para = "data"
    arquivo_necessario = "Anexo_I.pdf"
    caminho_pdf = os.path.join(extrair_para, arquivo_necessario)
    caminho_csv = "data/Anexo_I.csv"
    caminho_zip_final = "data/Teste_Katiane.zip"

    descompactar_zip(caminho_zip, extrair_para, arquivo_necessario)

    if not os.path.exists(caminho_pdf):
        print(f"Erro: O arquivo {caminho_pdf} não foi encontrado após a extração.")
        return

    legenda = extrair_legenda_do_pdf(caminho_pdf)    

    dados = extrair_dados_pdf(caminho_pdf)
    salvar_csv(dados, caminho_csv, legenda)
    print(f"Dados extraídos e salvos em {caminho_csv}")

    compactar_arquivo(caminho_csv, caminho_zip_final)
    print(f"Arquivo CSV compactado em {caminho_zip_final}")

    os.remove(caminho_pdf)
    os.remove(caminho_csv)

if __name__ == "__main__":
    main()