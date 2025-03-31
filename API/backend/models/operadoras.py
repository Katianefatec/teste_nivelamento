import pandas as pd
import os

def carregar_dados():
    
    base_dir = os.path.dirname(os.path.abspath(__file__))  
    possible_paths = [
        os.path.join(base_dir, "..", "data", "Relatorio_cadop.csv")  
    ]

    csv_path = None
    for path in possible_paths:
        if os.path.exists(path):
            csv_path = path
            break

    if not csv_path:
        raise FileNotFoundError("❌ Arquivo CSV não encontrado.")

    return pd.read_csv(csv_path, sep=";", dtype=str)