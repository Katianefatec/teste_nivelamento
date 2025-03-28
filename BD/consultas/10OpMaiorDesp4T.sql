USE ans_db;

SELECT
    o.Razao_Social,
    SUM(d.VL_SALDO_FINAL) AS Total_Despesas
FROM demonstracoes_contabeis d
JOIN operadoras o ON d.Reg_ANS = o.Registro_ANS
WHERE
    d.Descricao_CONTA_CONTABIL = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR '
    AND d.Data = '2024-12-31'
GROUP BY o.Razao_Social
ORDER BY Total_Despesas DESC
LIMIT 10;