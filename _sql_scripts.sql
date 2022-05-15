DROP DATABASE IF EXISTS DB_Leitor_Arquivos
CREATE DATABASE DB_Leitor_Arquivos;
GO

USE DB_Leitor_Arquivos;
GO

DROP TABLE IF EXISTS Arquivos
CREATE TABLE Arquivos
(
	ArquivoID INT NOT NULL IDENTITY(1, 1),
	NomeArquivo VARCHAR(400) NOT NULL,
	Observacao VARCHAR(200),
	DataCriacao DATETIME NOT NULL DEFAULT GETDATE()

	CONSTRAINT PK_ArquivoID PRIMARY KEY(ArquivoID)
);

DROP TABLE IF EXISTS Arquivos_Leitura
CREATE TABLE Arquivos_Leitura
(
	Arquivo_LeituraID INT NOT NULL IDENTITY(1, 1),
	ArquivoID INT NOT NULL,
	LeituraFinalizada BIT NOT NULL DEFAULT 0,
	RemetenteCpfCnpj VARCHAR(14),
	RemetenteInscEstadual VARCHAR(14),
	RemetenteRazaoSocial VARCHAR(200),
	DestinatarioNome VARCHAR(200),
	DestinatarioCpfCnpj VARCHAR(14),
	DestinatarioInscEstadual VARCHAR(14),
	RemetenteCep VARCHAR(8),
	RemetenteLogradouro VARCHAR(200),
	RemetenteNumero VARCHAR(15),
	RemetenteComplemento VARCHAR(50),
	RemetenteBairro VARCHAR(50),
	RemetenteCidade VARCHAR(50),
	RemetenteEstado VARCHAR(2),
	DestinatarioCep VARCHAR(8),
	DestinatarioLogradouro VARCHAR(200),
	DestinatarioNumero VARCHAR(15),
	DestinatarioComplemento VARCHAR(50),
	DestinatarioBairro VARCHAR(50),
	DestinatarioCidade VARCHAR(50),
	DestinatarioEstado VARCHAR(2),
	NumeroOrdem VARCHAR(50),
	Preco VARCHAR(15),
	ChaveNFe VARCHAR(50),
	DataCriacao DATETIME NOT NULL DEFAULT GETDATE()

	CONSTRAINT PK_Arquivo_LeituraID PRIMARY KEY(Arquivo_LeituraID)

	CONSTRAINT FK_Arquivos_Leitura_ArquivoID FOREIGN KEY(ArquivoID)
	REFERENCES Arquivos(ArquivoID)
);

DROP TABLE IF EXISTS Arquivos_Leitura_Items
CREATE TABLE Arquivos_Leitura_Items
(
	Arquivo_Leitura_ItemID INT NOT NULL IDENTITY(1, 1),
	Arquivo_LeituraID INT NOT NULL,
	Quantidade VARCHAR(5),
	CodigoItem VARCHAR(60),
	Descricao VARCHAR(100),
	DataCriacao DATETIME NOT NULL DEFAULT GETDATE()

	CONSTRAINT PK_Arquivo_Leitura_ItemID PRIMARY KEY(Arquivo_Leitura_ItemID)

	CONSTRAINT FK_Arquivos_Leitura_Items_Arquivo_LeituraID FOREIGN KEY(Arquivo_LeituraID)
	REFERENCES Arquivos_Leitura(Arquivo_LeituraID)
);