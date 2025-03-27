DROP DATABASE IF EXISTS ans_db;
CREATE DATABASE IF NOT EXISTS ans_db;
USE ans_db;

-- Tabela para dados cadastrais das operadoras
CREATE TABLE operadoras (
    Registro_ANS VARCHAR(10) PRIMARY KEY,
    CNPJ VARCHAR(20),
    Razao_Social VARCHAR(255),
    Nome_Fantasia VARCHAR(255),
    Modalidade VARCHAR(100),
    Logradouro VARCHAR(255),
    Numero VARCHAR(10),
    Complemento VARCHAR(100),
    Bairro VARCHAR(100),
    Cidade VARCHAR(100),
    UF CHAR(2),
    CEP VARCHAR(10),
    DDD VARCHAR(2),
    Telefone VARCHAR(20),
    Fax VARCHAR(20),
    Email VARCHAR(255),
    Representante VARCHAR(255),
    Cargo_Representante VARCHAR(100),
    Data_Registro_ANS DATE
);

-- Tabela para demonstrações contábeis
CREATE TABLE demonstracoes_contabeis (
    Data DATE,
    Reg_ANS VARCHAR(10),
    CD_CONTA_CONTABIL VARCHAR(20),
    Descricao_CONTA_CONTABIL VARCHAR(255),
    VL_SALDO_INICIAL DECIMAL(15, 2),
    VL_SALDO_FINAL DECIMAL(15, 2),
    FOREIGN KEY (Reg_ANS) REFERENCES operadoras(Registro_ANS)
);