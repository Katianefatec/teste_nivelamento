def validar_parametros(parametros, valores_padrao):
    for chave, valor_padrao in valores_padrao.items():
        if chave not in parametros or not parametros[chave]:
            parametros[chave] = valor_padrao
    return parametros