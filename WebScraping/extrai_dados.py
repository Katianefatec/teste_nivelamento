import pdfplumber
import pandas as pd
import zipfile
import os
import re

# Função para substituir siglas e corrigir palavras quebradas
# Função corrigida
def tratar_dados(df, legenda):
    # Mantém apenas OD e AMB com descrições usando a legenda
    if 'OD' in df.columns:
        df['OD'] = df['OD'].replace({legenda.get('OD', 'OD'): legenda['OD']}, regex=True)
    if 'AMB' in df.columns:
        df['AMB'] = df['AMB'].replace({legenda.get('AMB', 'AMB'): legenda['AMB']}, regex=True)

    # Restante do código original...
    colunas_desejadas = ["PROCEDIMENTO", "RN (alteração)", "VIGÊNCIA", "OD", "AMB",
                        "HCO", "HSO", "REF", "PAC", "DUT", "SUBGRUPO", "GRUPO", "CAPITULO"]
    
    df = df.apply(lambda x: x.str.replace(r',\s?', ' ', regex=True) if x.dtype == "object" else x)
    df = df[df['PROCEDIMENTO'].str.contains('\S', na=False)]
    
    return df[colunas_desejadas]

def extrair_tabelas_pdf(pdf_path):
    """Extrai tabelas com ajustes de precisão"""
    dados = []
    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:
            # Ajuste fino na detecção de células
            tabelas = pagina.extract_tables({
                "vertical_strategy": "lines", 
                "horizontal_strategy": "lines",
                "explicit_vertical_lines": pagina.curves + pagina.edges,
                "snap_tolerance": 5,
                "join_tolerance": 10
            })
            
            for tabela in tabelas:
                for linha in tabela:
                    # Filtra linhas de legenda
                    if any('Legenda:' in str(cell) for cell in linha):
                        continue
                        
                    # Padroniza número de colunas
                    linha_tratada = [str(cell).strip().replace('\n', ' ') for cell in linha]
                    linha_tratada += [''] * (13 - len(linha))  # Completa com valores vazios
                    
                    dados.append({
                        "PROCEDIMENTO": linha_tratada[0],
                        "RN (alteração)": linha_tratada[1],
                        "VIGÊNCIA": linha_tratada[2],
                        "OD": linha_tratada[3],
                        "AMB": linha_tratada[4],
                        "HCO": linha_tratada[5],
                        "HSO": linha_tratada[6],
                        "REF": linha_tratada[7],
                        "PAC": linha_tratada[8],
                        "DUT": linha_tratada[9],
                        "SUBGRUPO": linha_tratada[10],
                        "GRUPO": linha_tratada[11],
                        "CAPITULO": linha_tratada[12]
                    })
    return dados

def extrair_legenda_do_pdf(pdf_path):
    """Extrai a legenda do rodapé do PDF"""
    with pdfplumber.open(pdf_path) as pdf:
        legenda = {}
        for pagina in pdf.pages:
            texto = pagina.extract_text() or ""
            if "Legenda:" in texto:
                linhas = texto.split('\n')
                for linha in linhas:
                    linha = linha.strip()
                    if ':' in linha and not linha.startswith("Legenda:"):
                        partes = linha.split(':', 1)
                        if len(partes) == 2:
                            sigla = partes[0].strip()
                            descricao = partes[1].strip()
                            legenda[sigla] = descricao
        return legenda


def salvar_csv(dados, caminho_csv, legenda):
    """Salva os dados em CSV"""
    df = pd.DataFrame(dados)
    df = tratar_dados(df, legenda)  # Passa a legenda para a função tratar_dados
    
    os.makedirs(os.path.dirname(caminho_csv), exist_ok=True)
    df.to_csv(caminho_csv, index=False, encoding='utf-8-sig')

def compactar_arquivo(caminho_arquivo, caminho_zip):
    """Compacta o arquivo em ZIP"""
    with zipfile.ZipFile(caminho_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(caminho_arquivo, os.path.basename(caminho_arquivo))

def main():
    caminho_zip = "data/Anexos_ANS.zip"
    extrair_para = "data"
    arquivo_necessario = "Anexo_I.pdf"
    caminho_pdf = os.path.join(extrair_para, arquivo_necessario)
    caminho_csv = "data/Anexo_I.csv"
    caminho_zip_final = "data/Teste_Katiane.zip"

    # Descompacta o PDF
    with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
        zip_ref.extract(arquivo_necessario, extrair_para)

    if not os.path.exists(caminho_pdf):
        print(f"Erro: Arquivo {caminho_pdf} não encontrado!")
        return

    # Processa o PDF
    legenda = extrair_legenda_do_pdf(caminho_pdf)
    print("Legenda encontrada:", legenda)

    dados = extrair_tabelas_pdf(caminho_pdf)
    print(f"Extraídos {len(dados)} registros")

    if not dados:
        print("Nenhum dado extraído - verifique o formato do PDF")
        return

    # Tratar os dados
    df = pd.DataFrame(dados)
    df_tratado = tratar_dados(df, legenda)

    salvar_csv(df_tratado, caminho_csv, legenda)
    print(f"CSV salvo em {caminho_csv}")

    compactar_arquivo(caminho_csv, caminho_zip_final)
    print(f"Arquivo compactado em {caminho_zip_final}")

    # Limpeza
    os.remove(caminho_pdf)
    os.remove(caminho_csv)

if __name__ == "__main__":
    main()