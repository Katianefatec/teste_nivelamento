import pdfplumber
import pandas as pd
import zipfile
import os
import re

def extrair_tabelas_pdf(pdf_path):
    """Extrai tabelas do PDF com ajustes para evitar cabeçalhos duplicados"""
    dados = []
    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:
            tabelas = pagina.extract_tables({
                "vertical_strategy": "lines", 
                "horizontal_strategy": "lines",
                "explicit_vertical_lines": pagina.curves + pagina.edges,
                "snap_tolerance": 5,
                "join_tolerance": 10
            })
            
            for tabela in tabelas:
                for linha in tabela:
                    # Ignora cabeçalhos repetidos
                    if linha[0] == "PROCEDIMENTO":
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

def limpar_e_substituir_siglas(df, legenda):
    """Limpa todas as siglas e depois substitui apenas OD e AMB pelas descrições"""
    # Primeiro limpa TODAS as colunas (mantém apenas a sigla ou valor vazio)
    siglas_colunas = ['OD', 'AMB', 'HCO', 'HSO', 'REF', 'PAC', 'DUT']
    
    # Função para extrair apenas a sigla de uma string
    def extrair_sigla(texto, sigla):
        if not isinstance(texto, str):
            return texto
        # Se o texto contém a sigla, retorna apenas a sigla
        if sigla in texto:
            return sigla
        # Se não contém a sigla, mantém o texto original (pode ser vazio ou outro valor)
        return texto
    
    # Limpa todas as colunas de siglas primeiro
    for coluna in siglas_colunas:
        if coluna in df.columns:
            df[coluna] = df[coluna].apply(lambda x: extrair_sigla(x, coluna))
    
    # Depois substitui OD e AMB pelas descrições completas
    if 'OD' in df.columns and 'OD' in legenda:
        df['OD'] = df['OD'].apply(lambda x: legenda['OD'] if x == 'OD' else x)
    
    if 'AMB' in df.columns and 'AMB' in legenda:
        df['AMB'] = df['AMB'].apply(lambda x: legenda['AMB'] if x == 'AMB' else x)
    
    return df

def extrair_legenda_do_pdf(pdf_path):
    """Extrai a legenda do rodapé do PDF"""
    # Usar valores fixos garantidos para evitar problemas
    legenda = {
        "OD": "Seg. Odontológica",
        "AMB": "Seg. Ambulatorial",
        "HCO": "Seg. Hospitalar Com Obstetrícia",
        "HSO": "Seg. Hospitalar Sem Obstetrícia",
        "REF": "Plano Referência",
        "PAC": "Procedimento de Alta Complexidade",
        "DUT": "Diretriz de Utilização"
    }
    
    return legenda

def tratar_dados(df):
    """Trata os dados para corrigir quebras de linha e remover linhas inválidas"""
    # Corrige palavras quebradas
    for coluna in df.columns:
        for i in range(1, len(df)):
            if isinstance(df.at[i, coluna], str) and df.at[i, coluna].strip() and df.at[i, coluna].endswith(','):
                df.at[i - 1, coluna] = str(df.at[i - 1, coluna]) + ' ' + df.at[i, coluna].rstrip(',')
                df.at[i, coluna] = ''  # Limpa a linha atual
    
    # Remove linhas vazias
    df = df.dropna(how='all')
    df = df[df['PROCEDIMENTO'].str.strip().ne('')]
    
    return df

def salvar_csv(dados, caminho_csv, legenda):
    """Salva os dados em CSV com cabeçalho personalizado"""
    df = pd.DataFrame(dados)
    df = tratar_dados(df)  # Trata os dados primeiro
    df = limpar_e_substituir_siglas(df, legenda)  # Limpa as siglas e substitui OD e AMB
    
    # Renomeia as colunas OD e AMB para usar as descrições completas no cabeçalho
    rename_dict = {}
    if 'OD' in legenda:
        rename_dict['OD'] = legenda['OD']
    if 'AMB' in legenda:
        rename_dict['AMB'] = legenda['AMB']
    
    if rename_dict:
        df = df.rename(columns=rename_dict)
    
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

    salvar_csv(dados, caminho_csv, legenda)
    print(f"CSV salvo em {caminho_csv}")

    compactar_arquivo(caminho_csv, caminho_zip_final)
    print(f"Arquivo compactado em {caminho_zip_final}")

    # Limpeza
    os.remove(caminho_pdf)
    os.remove(caminho_csv)

if __name__ == "__main__":
    main()