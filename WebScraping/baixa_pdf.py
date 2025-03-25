import requests
import zipfile
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Configurações
BASE_URL = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
HEADERS = {'User-Agent': 'Mozilla/5.0'}
ZIP_NAME = "data/Anexos_ANS.zip"
ANEXOS = {
    "Anexo_I.pdf": {
        "texto_link": "Anexo I.",
        "url_part": "Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
    },
    "Anexo_II.pdf": {
        "texto_link": "Anexo II.",
        "url_part": "Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf"
    }
}

def obter_conteudo_pagina(url):
    """Obtém o conteúdo HTML da página"""
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def encontrar_url_anexo(soup, texto_link, url_part):
    """Encontra a URL do anexo com base no texto do link e parte da URL"""
    for link in soup.find_all('a', class_='internal-link', target='_blank'):
        if texto_link in link.get_text(strip=True) and url_part in link['href']:
            return link['href'] if link['href'].startswith('http') else urljoin(BASE_URL, link['href'])
    return None

def baixar_arquivo(url, filename):
    """Faz o download de um arquivo"""
    response = requests.get(url, headers=HEADERS, stream=True)
    response.raise_for_status()
    
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    
    return os.path.getsize(filename)

def main():
    try:
        print(f"Acessando {BASE_URL}...")
        soup = obter_conteudo_pagina(BASE_URL)
        
        arquivos_baixados = []
        
        for filename, data in ANEXOS.items():
            if url := encontrar_url_anexo(soup, data['texto_link'], data['url_part']):
                print(f"Baixando {filename}...")
                size = baixar_arquivo(url, filename) / 1024
                arquivos_baixados.append(filename)
                print(f"{filename} baixado ({size:.1f} KB)")
            else:
                print(f"{filename} não encontrado")

        if arquivos_baixados:
            # Cria o diretório data se não existir
            os.makedirs(os.path.dirname(ZIP_NAME), exist_ok=True)
            
            with zipfile.ZipFile(ZIP_NAME, 'w') as zipf:
                for file in arquivos_baixados:
                    zipf.write(file)
                    os.remove(file)
            print(f"\nArquivos compactados em {ZIP_NAME}")
        else:
            print("\nNenhum arquivo foi baixado")

    except Exception as e:
        print(f"\nErro: {str(e)}")

if __name__ == "__main__":
    main()