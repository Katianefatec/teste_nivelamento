from flask import Blueprint, request, jsonify
import pandas as pd
from models.operadoras import carregar_dados

# Criar o blueprint
bp_operadoras = Blueprint('operadoras', __name__)

# Carregar os dados
df = carregar_dados()

@bp_operadoras.route('/api/operadoras', methods=['GET'])
def listar_operadoras():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    sort_field = request.args.get('sort', 'Razao_Social')
    sort_order = request.args.get('order', 'asc')

    try:
        # Ordenar os dados
        resultados = df.sort_values(by=sort_field, ascending=(sort_order == 'asc'))

        # Paginação
        total = len(resultados)
        start = (page - 1) * limit
        end = start + limit
        paginated = resultados.iloc[start:end]

        # Converter para dicionário e tratar valores nulos
        records = []
        for _, row in paginated.iterrows():
            record = {}
            for col in paginated.columns:
                value = row[col]
                if pd.isna(value):
                    record[col] = None
                else:
                    record[col] = value
            records.append(record)

        print(f"Enviando {len(records)} registros para o frontend")
        
        return jsonify({
            "total": total,
            "totalPages": (total // limit) + (1 if total % limit > 0 else 0),
            "currentPage": page,
            "limit": limit,
            "results": records
        })
    except Exception as e:
        print(f"Erro ao processar requisição: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp_operadoras.route('/api/operadoras/busca', methods=['GET'])
def buscar_operadoras():
    termo = request.args.get('termo', '').lower()
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    sort_field = request.args.get('sort', 'Razao_Social')
    sort_order = request.args.get('order', 'asc')

    try:
        # Filtrar os dados com base no termo de busca
        resultados = df[df.apply(lambda row: termo in str(row).lower(), axis=1)]
        resultados = resultados.sort_values(by=sort_field, ascending=(sort_order == 'asc'))

        # Paginação
        total = len(resultados)
        start = (page - 1) * limit
        end = start + limit
        paginated = resultados.iloc[start:end]

        # Converter para dicionário e tratar valores nulos
        records = []
        for _, row in paginated.iterrows():
            record = {}
            for col in paginated.columns:
                value = row[col]
                if pd.isna(value):
                    record[col] = None
                else:
                    record[col] = value
            records.append(record)

        print(f"Enviando {len(records)} registros da busca para o frontend")
        
        return jsonify({
            "total": total,
            "totalPages": (total // limit) + (1 if total % limit > 0 else 0),
            "currentPage": page,
            "limit": limit,
            "results": records
        })
    except Exception as e:
        print(f"Erro na busca: {str(e)}")
        return jsonify({"error": str(e)}), 500