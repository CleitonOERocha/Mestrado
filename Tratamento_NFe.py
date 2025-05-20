


import warnings
warnings.simplefilter(action='ignore')
import os
import pandas as pd
import numpy as np
from glob import glob
from tqdm import tqdm

###################################################################
#### Class --------------------------------------------------------
###################################################################

class Tratamento_NFe:

    '''
    Função para fazer o tratamento dos arquivos baixados com o código Download_Extracao_NFe.py

    Argumentos:

    * ano = Ano que deseja gerar o arquivo. Usar no formato str. Exemplo "2024", "2023", etc.
    * arquivo_empresas = Nome do arquivo gerado no código Tratamento_Empresas_Punidas.py.
    * retornar_dataframe = True/False. Use para retornar o dataframe no ambiente de execução.
    * salvar_xlsx = True/False. Use para salvar o dataframe gerado em um arquivo xlsx.
    * pasta_para_salvar = None / Pasta desejada. Use 'None' para salvar o xlsx na pasta de execução do código ou \
                          passe um caminho para a pasta que deseja salvar o arquivo.

    Exemplo:

    * Executando e gerando um arquivo xlsx na pasta de execução do código:<br />
    Tratamento_NFe("2024", "empresas_punidas.xlsx", retornar_dataframe=False, save_parquet=True, pasta_para_salvar=None)<br />
    <br />
    * Executando e gerando somente o dataframe no ambiente de execução (sem gerar xlsx):<br />
    tnfe  = Tratamento_NFe("2024", "empresas_punidas.xlsx", retornar_dataframe=True, save_parquet=False, pasta_para_salvar=None)<br />
    df  = tnfe.df_nfe       

    '''

    def __init__(self, 
                 ano:str, 
                 arquivo_empresas:str, 
                 retornar_dataframe = False, 
                 save_parquet = True, 
                 pasta_para_salvar = None):

        if retornar_dataframe is False:

            self.executar_tratamento_arquivos_nfe(ano,
                                                  arquivo_empresas,
                                                  return_df = retornar_dataframe, 
                                                  save_parquet = save_parquet,
                                                  path_to_save = pasta_para_salvar)
        else:

            self.df_nfe = None

            self.df_nfe = self.executar_tratamento_arquivos_nfe(ano,
                                                                arquivo_empresas,
                                                                return_df = retornar_dataframe, 
                                                                save_parquet = save_parquet,
                                                                path_to_save = pasta_para_salvar)

    def tratar_arquivo_nfe(self, ano:str, arquivo_empresas:str):

        arquivos_pasta = glob(ano + '/*NotaFiscalItem.csv')

        df_final = pd.DataFrame()

        for i in tqdm(range(0, len(arquivos_pasta))):

            try:

                df = pd.read_csv(arquivos_pasta[i], 
                                sep=';', 
                                encoding='latin1', 
                                thousands='.', 
                                decimal=',')

                df = df[['NATUREZA DA OPERAÇÃO', 'DATA EMISSÃO', 'CPF/CNPJ Emitente',
                        'RAZÃO SOCIAL EMITENTE', 'UF EMITENTE', 'MUNICÍPIO EMITENTE',
                        'CNPJ DESTINATÁRIO', 'NOME DESTINATÁRIO', 'UF DESTINATÁRIO',
                        'CONSUMIDOR FINAL', 'NÚMERO PRODUTO', 'DESCRIÇÃO DO PRODUTO/SERVIÇO',
                        'CÓDIGO NCM/SH', 'NCM/SH (TIPO DE PRODUTO)', 'CFOP',
                        'QUANTIDADE', 'UNIDADE', 'VALOR UNITÁRIO', 'VALOR TOTAL']]
                
                df = df.rename(columns = {'NATUREZA DA OPERAÇÃO':'natureza_operacao',
                                        'DATA EMISSÃO':'data_emissao',
                                        'CPF/CNPJ Emitente':'cnpj_cpf_emitente',
                                        'RAZÃO SOCIAL EMITENTE':'razao_social_emitente',
                                        'UF EMITENTE':'uf_emitente', 
                                        'MUNICÍPIO EMITENTE':'mun_emitente',
                                        'CNPJ DESTINATÁRIO':'cnpj_destinario', 
                                        'NOME DESTINATÁRIO':'nome_destinatario',
                                        'UF DESTINATÁRIO':'uf_destinatario',
                                        'CONSUMIDOR FINAL':'consumidor_final',
                                        'NÚMERO PRODUTO':'numero_produto',
                                        'DESCRIÇÃO DO PRODUTO/SERVIÇO':'descricao_produto',
                                        'CÓDIGO NCM/SH':'codigo_ncm', 
                                        'NCM/SH (TIPO DE PRODUTO)':'ncm_produto',
                                        'CFOP':'cpof', 
                                        'QUANTIDADE':'quantidade', 
                                        'UNIDADE':'unidade',
                                        'VALOR UNITÁRIO':'valor_unitario', 
                                        'VALOR TOTAL':'valor_total'})

                df = (df
                    .dropna(subset = 'ncm_produto')
                    .reset_index(drop=True))

                df['data_emissao'] = (pd
                                     .to_datetime(df['data_emissao'], dayfirst=True)
                                     .dt
                                     .strftime('%Y-%m-%d'))
                
                df['cnpj_cpf_emitente'] = df['cnpj_cpf_emitente'].astype(str)

                df['cnpj_destinario'] = (df['cnpj_destinario'].astype('int64'))

                df['cnpj_destinario'] = (df['cnpj_destinario'].astype('str'))

                df['cnpj_destinario'] = (df['cnpj_destinario'].str.rjust(14, "0"))

                df_final = pd.concat([df_final, df], ignore_index=True)

            except Exception as error:

                print("Erro no arquivo ", i, '\n Log do erro:', error)

        # Inserindo informação de status do CNPJ -------------------------------------------------
        df_empresas = pd.read_excel(arquivo_empresas)

        df_empresas['cnpj'] = (df_empresas['cnpj'].astype('int64'))

        df_empresas['cnpj'] = (df_empresas['cnpj'].astype('str'))

        # Se o CNPJ não tem 14 digitos, insere 0 a esquerda até completar ----------
        df_empresas['cnpj'] = (df_empresas['cnpj']
                                        .str
                                        .rjust(14,"0"))

        df_empresas = df_empresas.rename(columns={'cnpj':'cnpj_cpf_emitente'})

        df_final_empresas = pd.merge(df_final, df_empresas, how='left', on='cnpj_cpf_emitente')

        df_final_empresas['classe'] = np.where(df_final_empresas['classe'].isna(), 0, 1)   

        # Criando coluna de text com infos ---------------------------------------------------
        df_final_empresas['text'] = ('[CLS] ' +
                                    'Natureza da operacao: ' + df_final_empresas['natureza_operacao'] + ' [SEP] ' +
                                    'Destinatario: ' + df_final_empresas['nome_destinatario'] + ' [SEP] ' +
                                    'Municipio emitente: ' + df_final_empresas['mun_emitente'] + ' [SEP] ' +
                                    'Numero do produto: ' + df_final_empresas['numero_produto'].astype(str) + ' [SEP] ' +
                                    'Descricao do produto: ' + df_final_empresas['descricao_produto'] + ' [SEP] ' +
                                    'Codigo NCM: ' + df_final_empresas['codigo_ncm'].astype(str) + ' [SEP] ' +
                                    'NCM do produto: ' + df_final_empresas['ncm_produto'] + ' [SEP] ' + 
                                    'Tipo und: ' + df_final_empresas['unidade'] + ' [SEP] ' + 
                                    'Valor unitario: ' + df_final_empresas['valor_unitario'].astype(str) + ' [SEP] ' + 
                                    'Quantidade: ' + df_final_empresas['quantidade'].astype(str) + ' [SEP] ' + 
                                    'Total: ' + df_final_empresas['valor_total'].astype(str))
        
        df_final_empresas = df_final_empresas[['natureza_operacao', 'data_emissao', 'cnpj_cpf_emitente',
                                               'razao_social_emitente', 'uf_emitente', 'mun_emitente',
                                               'nome_destinatario', 'descricao_produto',
                                               'ncm_produto', 'quantidade', 'valor_unitario', 'valor_total',
                                               'classe', 'text']]
        
        return df_final_empresas

    def executar_tratamento_arquivos_nfe(self,
                                         ano:str,
                                         arquivo_empresas:str,
                                         return_df = False, 
                                         save_parquet = True, 
                                         path_to_save = None):
        
        df_nfe_tratado = self.tratar_arquivo_nfe(ano, arquivo_empresas)

        if return_df is True:

            return df_nfe_tratado
        
        if save_parquet is True and path_to_save is None:

            df_nfe_tratado.to_parquet(f'Notas_Fiscais_Itens_{ano}.parquet', index=False)

            print(f"Arquivo 'Notas_Fiscais_Itens_{ano}.parquet' gerado com sucesso!")

        elif save_parquet is True and path_to_save is not None:

            df_nfe_tratado.to_parquet(os.path.join(path_to_save, f'Notas_Fiscais_Itens_{ano}.parquet'), 
                                      index=False)

            print(f"Arquivo 'Notas_Fiscais_Itens_{ano}.parquet' gerado com sucesso na pasta solicitada!")

        elif save_parquet is False and path_to_save is not None:

            print("Use 'save_parquet = True' para salvar o arquivo no diretório escolhido.")

        elif save_parquet is False and path_to_save is None and return_df is False:

            print("Use 'save_parquet = True' para salvar o arquivo ou 'return_df = True' para obter o dataframe.")