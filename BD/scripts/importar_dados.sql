USE ans_db;

-- Importar dados cadastrais das operadoras 
LOAD DATA LOCAL INFILE '../dados/dados_cadastrais_ANS/Relatorio_cadop.csv'
INTO TABLE operadoras
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    Registro_ANS, CNPJ, Razao_Social, Nome_Fantasia, Modalidade,
    Logradouro, Numero, Complemento, Bairro, Cidade, UF, CEP,
    DDD, Telefone, Fax, Email, Representante, Cargo_Representante,
    @Data_Registro_ANS
)
SET Data_Registro_ANS = STR_TO_DATE(@Data_Registro_ANS, '%d/%m/%Y');

-- Importar demonstrações contábeis diretamente
LOAD DATA LOCAL INFILE '../dados/dem_contabeis_2023_2024/1T2023.csv'
INTO TABLE demonstracoes_contabeis
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@data, Reg_ANS, CD_CONTA_CONTABIL, Descricao_CONTA_CONTABIL, @vl_inicial, @vl_final)
SET 
    Data = '2023-03-31',
    VL_SALDO_INICIAL = REPLACE(REPLACE(@vl_inicial, ".", ""), ",", "."),
    VL_SALDO_FINAL = REPLACE(REPLACE(@vl_final, ".", ""), ",", ".");

LOAD DATA LOCAL INFILE '../dados/dem_contabeis_2023_2024/2T2023.csv'
INTO TABLE demonstracoes_contabeis
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@data, Reg_ANS, CD_CONTA_CONTABIL, Descricao_CONTA_CONTABIL, @vl_inicial, @vl_final)
SET 
    Data = '2023-06-30',
    VL_SALDO_INICIAL = REPLACE(REPLACE(@vl_inicial, ".", ""), ",", "."),
    VL_SALDO_FINAL = REPLACE(REPLACE(@vl_final, ".", ""), ",", ".");

LOAD DATA LOCAL INFILE '../dados/dem_contabeis_2023_2024/3T2023.csv'
INTO TABLE demonstracoes_contabeis
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@data, Reg_ANS, CD_CONTA_CONTABIL, Descricao_CONTA_CONTABIL, @vl_inicial, @vl_final)
SET 
    Data = '2023-09-30',
    VL_SALDO_INICIAL = REPLACE(REPLACE(@vl_inicial, ".", ""), ",", "."),
    VL_SALDO_FINAL = REPLACE(REPLACE(@vl_final, ".", ""), ",", ".");

LOAD DATA LOCAL INFILE '../dados/dem_contabeis_2023_2024/4T2023.csv'
INTO TABLE demonstracoes_contabeis
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@data, Reg_ANS, CD_CONTA_CONTABIL, Descricao_CONTA_CONTABIL, @vl_inicial, @vl_final)
SET 
    Data = '2023-12-31',
    VL_SALDO_INICIAL = REPLACE(REPLACE(@vl_inicial, ".", ""), ",", "."),
    VL_SALDO_FINAL = REPLACE(REPLACE(@vl_final, ".", ""), ",", ".");


LOAD DATA LOCAL INFILE '../dados/dem_contabeis_2023_2024/1T2024.csv'
INTO TABLE demonstracoes_contabeis
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@data, Reg_ANS, CD_CONTA_CONTABIL, Descricao_CONTA_CONTABIL, @vl_inicial, @vl_final)
SET 
    Data = '2024-03-31',
    VL_SALDO_INICIAL = REPLACE(REPLACE(@vl_inicial, ".", ""), ",", "."),
    VL_SALDO_FINAL = REPLACE(REPLACE(@vl_final, ".", ""), ",", ".");

LOAD DATA LOCAL INFILE '../dados/dem_contabeis_2023_2024/2T2024.csv'
INTO TABLE demonstracoes_contabeis
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@data, Reg_ANS, CD_CONTA_CONTABIL, Descricao_CONTA_CONTABIL, @vl_inicial, @vl_final)       

SET 
    Data = '2024-06-30',
    VL_SALDO_INICIAL = REPLACE(REPLACE(@vl_inicial, ".", ""), ",", "."),
    VL_SALDO_FINAL = REPLACE(REPLACE(@vl_final, ".", ""), ",", ".");

LOAD DATA LOCAL INFILE '../dados/dem_contabeis_2023_2024/3T2024.csv'
INTO TABLE demonstracoes_contabeis
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@data, Reg_ANS, CD_CONTA_CONTABIL, Descricao_CONTA_CONTABIL, @vl_inicial, @vl_final)
SET 
    Data = '2024-09-30',
    VL_SALDO_INICIAL = REPLACE(REPLACE(@vl_inicial, ".", ""), ",", "."),
    VL_SALDO_FINAL = REPLACE(REPLACE(@vl_final, ".", ""), ",", ".");

LOAD DATA LOCAL INFILE '../dados/dem_contabeis_2023_2024/4T2024.csv'
INTO TABLE demonstracoes_contabeis
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'        
IGNORE 1 ROWS
(@data, Reg_ANS, CD_CONTA_CONTABIL, Descricao_CONTA_CONTABIL, @vl_inicial, @vl_final)
SET 
    Data = '2024-12-31',
    VL_SALDO_INICIAL = REPLACE(REPLACE(@vl_inicial, ".", ""), ",", "."),
    VL_SALDO_FINAL = REPLACE(REPLACE(@vl_final, ".", ""), ",", ".");

-- Desativar o modo de atualização segura
SET SQL_SAFE_UPDATES = 0;

-- Atualizar a coluna Descricao_CONTA_CONTABIL para remover espaços extras
UPDATE demonstracoes_contabeis
SET Descricao_CONTA_CONTABIL = REPLACE(Descricao_CONTA_CONTABIL, '  ', ' ')
WHERE Descricao_CONTA_CONTABIL LIKE '%SINISTROS CONHECIDOS%';

UPDATE demonstracoes_contabeis
SET Descricao_CONTA_CONTABIL = TRIM(Descricao_CONTA_CONTABIL)
WHERE Descricao_CONTA_CONTABIL LIKE '%SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%';

-- Reativar o modo de atualização segura (opcional)
SET SQL_SAFE_UPDATES = 1;


    