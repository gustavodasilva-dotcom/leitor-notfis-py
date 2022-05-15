#!/usr/bin/env python
# coding: utf-8

# In[8]:


# Instalando pyodbc para conectar ao SQL Server.
import pyodbc
# Instalando pyodbc para conectar ao SQL Server.


# Declaração de variáveis globais
layout = str()
id_arquivo = int()
id_leitura = int()
arquivo = 'C:\\Leitor\\ClienteFicticioNOTFIS\\PROCESSED\\2022\\3\\22\\2910211052-571343-136047-Origem-135624 (1).txt'
# Declaração de variáveis globais


# Criando conexão ao banco
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-8J62RD3\SQLEXPRESS;'
                      'Database=DB_Leitor_Arquivos;'
                      'Trusted_Connection=yes')
cursor = conn.cursor()
# Criando conexão ao banco


# Funções de banco de dados
def inserir_log_arquivo(arquivo):
    """
    Função responsável por inserir, no momento da leitura do arquivo, o log de leitura.
    """
    id = 0
    try:
        cursor.execute("INSERT INTO Arquivos (NomeArquivo) VALUES ('{}');".format(arquivo));
        cursor.execute("SELECT @@IDENTITY AS ID;")
        id = cursor.fetchone()[0]
        cursor.commit()
        if id != 0:
            print('Registro do arquivo inserido com sucesso. ID: {0}.'.format(str(id)))
        else:
            print('Ocorreu um erro ao registrar o log do arquivo {}.'.format(arquivo))
    except:
        cursor.rollback()
        print('Ocorreu um erro ao realizar a conexão com o banco de dados. Método = {}.'.format('inserir_log_arquivo'));
    return id

def inserir_leitura(id_arquivo):
    """
    Função responsável por inserir os dados coletados, linha a linha, do arquivo.
    """
    id = 0
    try:
        cursor.execute("INSERT INTO Arquivos_Leitura (ArquivoID) VALUES ({});".format(int(id_arquivo)));
        cursor.execute("SELECT @@IDENTITY AS ID;")
        id = cursor.fetchone()[0]
        cursor.commit()
        if id != 0:
            print('Registro de leitura do arquivo inserido com sucesso. ID: {0}.'.format(str(id)))
        else:
            print('Ocorreu um erro ao registrar o log de leitura do arquivo {}.'.format(arquivo))
    except:
        cursor.rollback()
        print('Ocorreu um erro ao realizar a conexão com o banco de dados. Método = {}.'.format('inserir_leitura'));
    return id

def atualizar_log_arquivo(mensagem):
    """
    Função responsável por atualizar a observação no log de leitura do arquivo.
    """
    try:
        cursor.execute("UPDATE Arquivos SET Observacao = '{0}' WHERE ArquivoID = {1};".format(mensagem, id_arquivo))
        cursor.commit()
        print('Observação atualizada com sucesso no registro {}.'.format(int(id_arquivo)))
    except:
        cursor.rollback()
        print('Ocorreu um erro ao realizar a conexão com o banco de dados. Método = {}.'.format('atualizar_log_arquivo'));
        
def executar_db(comando):
    """
    Função responsável por executar um comando no banco de dados do SQL Server.
    """
    try:
        cont = cursor.execute(comando).rowcount
        cursor.commit()
        return cont
    except:
        cursor.rollback()
        print('Ocorreu um erro ao realizar a conexão com o banco de dados. Método = {}.'.format('executar_db'));
    
# Funções de banco de dados
        

# Definindo funções
def obter_layout(conteudo):
    """
    Função que obtém, especificamente, a segunda linha do arquivo, e, com base na primeira posição da linha,
    especificar o layout do arquivo Proceda NOTFIS.
    """
    cont = 0
    for l in conteudo:
        cont += 1
        if cont == 2:
            global layout
            layout = l[:1]
    return layout

def processar_layout_3():
    """
    Função responsável por ler e processar o layout 3 do arquivo Proceda NOTFIS.
    """
    id_leitura = 0
    cont_lin_311 = 0
    cont_lin_312 = 0
    cont_lin_313 = 0
    conteudo = open(arquivo, 'r')
    for l in conteudo:
        if l[:3] == '311':
            if id_leitura == 0:
                id_leitura = inserir_leitura(id_arquivo)
                cont_lin_311 += 1
                try:
                    resultado = executar_db("""
                    UPDATE Arquivos_Leitura
                    SET
                         RemetenteCpfCnpj = '{0}'
                        ,RemetenteInscEstadual = '{1}'
                        ,RemetenteRazaoSocial = '{2}'
                        ,RemetenteCep = '{3}'
                        ,RemetenteLogradouro = '{4}'
                        ,RemetenteCidade = '{5}'
                        ,RemetenteEstado = '{6}'
                    WHERE Arquivo_LeituraID = {7};
                    """.format(l[3:17], l[17:29], l[133:173], l[107:115], l[32:72], l[72:107], l[116:118], id_leitura))
                    if resultado > 0:
                        print('Linha 311 -> Inserida e informações atualizadas. ArquivoID: {0} -- Pedido {1}.'.format(id_arquivo, cont_lin_311))
                    else:
                        print('Linha 311 -> Informações não foram inseridas. ArquivoID: {0} -- Pedido {1}.'.format(id_arquivo, cont_lin_311))
                except:
                    print('Linha 311 -> Exceção ao atualizar informações. ArquivoID: {0} - Pedido {1}.'.format(id_arquivo, cont_lin_311))
        if l[:3] == '312':
            try:
                cont_lin_312 += 1
                resultado = executar_db("""
                UPDATE Arquivos_Leitura
                SET
                     DestinatarioNome = '{0}'
                    ,DestinatarioCpfCnpj = '{1}'
                    ,DestinatarioInscEstadual = '{2}'
                    ,DestinatarioCep = '{3}'
                    ,DestinatarioLogradouro = '{4}'
                    ,DestinatarioNumero = '{5}'
                    ,DestinatarioComplemento = '{6}'
                    ,DestinatarioBairro = '{7}'
                    ,DestinatarioCidade = '{8}'
                    ,DestinatarioEstado = '{9}'
                WHERE Arquivo_LeituraID = {10};
                """.format(l[3:43], l[43:57], l[57:72], l[167:185], l[72:112], l[294:300], l[240:294], l[112:132], l[132:167], l[185:187], id_leitura))
                if resultado > 0:
                    print('Linha 312 -> Inserida e informações atualizadas. ArquivoID: {0} -- Pedido {1}.'.format(id_arquivo, cont_lin_311))
                else:
                    print('Linha 312 -> Informações não foram inseridas. ArquivoID: {0} -- Pedido {1}.'.format(id_arquivo, cont_lin_311))
            except:
                print('Linha 312 -> Exceção ao atualizar informações. ArquivoID: {0} - Pedido {1}.'.format(id_arquivo, cont_lin_311))
        elif l[:3] == '307':
            try:
                numero_ordem = l[108:189]
                executar_db("""
                UPDATE Arquivos_Leitura
                SET
                    NumeroOrdem = '{0}'
                WHERE Arquivo_LeituraID = {1};
                """.format(numero_ordem.strip(), id_leitura))
                if resultado > 0:
                    print('Linha 307 -> Informações inseridas. ArquivoID: {0} - Pedido {1}.'.format(id_arquivo, cont_lin_311))
                else:
                    print('Linha 307 -> Informações não foram inseridas. ArquivoID: {0} - Pedido {1}.'.format(id_arquivo, cont_lin_311))
            except:
                print('Linha 307 -> Exceção ao atualizar informações. ArquivoID: {0} - Pedido {1}.'.format(id_arquivo, cont_lin_311))
        elif l[:3] == '313':
            cont_lin_313 += 1
            try:
                executar_db("""
                    UPDATE Arquivos_Leitura
                    SET
                         Preco = '{0}'
                        ,ChaveNFe = '{1}'
                    WHERE Arquivo_LeituraID = {2};
                """.format(l[85:100], l[258:302], id_leitura))
            except:
                print('Linha 313 -> Exceção ao inserir informações. ArquivoID: {0} - Pedido {1}.'.format(id_arquivo, cont_lin_311))
        elif l[:3] == '314':
            try:
                desc_item = str()
                numerico = l[25:34].isnumeric()
                if numerico:
                    desc_item = l[25:34]
                else:
                    desc_item = l[25:107]
                executar_db(
                """
                INSERT INTO Arquivos_Leitura_Items
                (
                     Arquivo_LeituraID
                    ,Quantidade
                    ,Descricao
                )
                VALUES
                (
                      {0}
                    ,'{1}'
                    ,'{2}'
                );
                """.format(id_leitura, l[5:10], desc_item))
                if resultado > 0:
                    print('Linha 314 -> Informações inseridas. ArquivoID: {0} -- Pedido {1}.'.format(id_arquivo, cont_lin_311))
                else:
                    print('Linha 314 -> Informações não foram inseridas. ArquivoID: {0} -- Pedido {1}.'.format(id_arquivo, cont_lin_311))
            except:
                print('Linha 314 -> Exceção ao inserir informações. ArquivoID: {0} - Pedido {1}.'.format(id_arquivo, cont_lin_311))
        elif l[:3] == '319':
            if id_leitura > 0:
                resultado = executar_db('UPDATE Arquivos_Leitura SET LeituraFinalizada = 1 WHERE Arquivo_LeituraID = {};'.format(id_leitura))
                if resultado > 0:
                    print('Leitura finalizada. ArquivoID: {0} -- Pedido {1}.'.format(id_arquivo, cont_lin_311))
                else:
                    print('Linha 319 -> Informações não foram inseridas. ArquivoID: {0} -- Pedido {1}.'.format(id_arquivo, cont_lin_311))
                id_leitura = 0
        
def processar_layout_5():
    """
    Função responsável por ler e processar o layout 5 do arquivo Proceda NOTFIS.
    """
    conteudo = open(arquivo, 'r')
# Definindo funções


# Main
conteudo = str()
try:
    conteudo = open(arquivo, 'r')
except:
    print('Ocorreu um erro ao abrir e ler o arquivo {}.'.format(arquivo));
print("Iniciando leitura do arquivo {0}.".format(arquivo))
id_arquivo = inserir_log_arquivo(arquivo)
if id_arquivo != 0:
    layout = obter_layout(conteudo)
    if layout == '3':
        processar_layout_3()
    elif layout == '5':
        processar_layout_5()
    else:
        atualizar_log_arquivo('O arquivo não é Proceda NOTFIS do layout 3 ou 5.')
# Main


# In[ ]:




