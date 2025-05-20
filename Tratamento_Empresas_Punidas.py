

import os
import pandas as pd
from glob import glob
import datetime

###################################################################
#### Class --------------------------------------------------------
###################################################################

class Tratamento_Empresas_Punidas:
    
    '''
    Função para fazer o tratamento dos arquivos baixados com o código Download_Empresas_Punidas.py

    Argumentos:

    * retornar_dataframe = True/False. Use para retornar o dataframe no ambiente de execução.
    * salvar_xlsx = True/False. Use para salvar o dataframe gerado em um arquivo xlsx.
    * pasta_para_salvar = None / Pasta desejada. Use 'None' para salvar o xlsx na pasta de execução do código ou \
                          passe um caminho para a pasta que deseja salvar o arquivo.

    Exemplo:

    * Executando e gerando um arquivo xlsx na pasta de execução do código:
    Tratamento_Empresas_Punidas(retornar_dataframe=False, salvar_xlsx=True, pasta_para_salvar=None)<br />
    <br />
    * Executando e gerando somente o dataframe no ambiente de execução (sem gerar xlsx):<br />
    tep  = Tratamento_Empresas_Punidas(retornar_dataframe=True, salvar_xlsx=False, pasta_para_salvar=None)<br />
    df  = tep.df_empresas       

    '''

    def __init__(self, retornar_dataframe = False, salvar_xlsx = True, pasta_para_salvar=None):

        df_inid, df_punidas, df_sem_fin_luc = self.obter_arquivos_recentes()

        if retornar_dataframe is False:

            self.executar_tratamento_arquivos(df_inid, 
                                              df_punidas, 
                                              df_sem_fin_luc, 
                                              return_df = retornar_dataframe, 
                                              save_xlsx = salvar_xlsx,
                                              path_to_save = pasta_para_salvar)
        else:

            self.df_empresas = None

            self.df_empresas = self.executar_tratamento_arquivos(df_inid, 
                                                                 df_punidas, 
                                                                 df_sem_fin_luc, 
                                                                 return_df = retornar_dataframe, 
                                                                 save_xlsx = salvar_xlsx,
                                                                 path_to_save = pasta_para_salvar)
                
    # Obter os arquivos mais recentes
    def obter_arquivos_recentes(self):

        arquivos_cnep = glob("CNEP/*.csv")
        arquivos_cepim = glob("CEPIM/*.csv")
        arquivos_ceis = glob("CEIS/*.csv")
    
        mais_recente_cnep = max(arquivos_cnep,
                                key=lambda f: datetime.datetime.strptime(f.split("_")[0].split("\\")[-1], 
                                                                         "%Y%m%d"))

        mais_recente_cepim = max(arquivos_cepim,
                                 key=lambda f: datetime.datetime.strptime(f.split("_")[0].split("\\")[-1], 
                                                                         "%Y%m%d"))

        mais_recente_ceis = max(arquivos_ceis,
                                key=lambda f: datetime.datetime.strptime(f.split("_")[0].split("\\")[-1], 
                                                                         "%Y%m%d"))
        
        df_inid = pd.read_csv(mais_recente_ceis, sep=';', encoding='latin1')
        df_punidas = pd.read_csv(mais_recente_cnep, sep=';', encoding='latin1')
        df_sem_fin_luc = pd.read_csv(mais_recente_cepim, sep=';', encoding='latin1')

        return df_inid, df_punidas, df_sem_fin_luc

    # Empresas Inidôneas e Suspensas
    def tratar_arquivo_ceis(self, df_inid:pd.DataFrame):

        df_inid = (df_inid
                    .rename(columns={'CPF OU CNPJ DO SANCIONADO':'cnpj'}))

        df_inid = df_inid.dropna(subset = 'cnpj').reset_index(drop=True)                           

        df_inid = df_inid.assign(cnpj = df_inid['cnpj'].astype(str))

        df_inid['cnpj'] = (df_inid['cnpj']
                            .replace(to_replace='\\.', value='', regex=True)
                            .replace(to_replace='-', value='', regex=True)
                            .replace(to_replace='\/', value='', regex=True))

        df_inid['cnpj'] = df_inid['cnpj'].astype('int64')
        df_inid['cnpj'] = df_inid['cnpj'].astype('str')  

        df_inid['cnpj'] = (df_inid['cnpj'].str.rjust(14,"0"))       

        df_inid = (df_inid[['cnpj']]
                    .drop_duplicates(subset='cnpj')
                    .reset_index(drop=True)
                    .assign(classe = 'Empresa Inidônea'))
        
        return df_inid

    # Empresas Punidas
    def tratar_arquivo_cnep(self, df_punidas:pd.DataFrame):

        df_punidas = (df_punidas
                    .rename(columns={'CPF OU CNPJ DO SANCIONADO':'cnpj'}))

        df_punidas = df_punidas.assign(cnpj = df_punidas['cnpj'].astype(str))

        df_punidas['cnpj'] = (df_punidas['cnpj']
                            .replace(to_replace='\\.', value='', regex=True)
                            .replace(to_replace='-', value='', regex=True)
                            .replace(to_replace='\/', value='', regex=True))

        df_punidas = df_punidas.dropna(subset = 'cnpj').reset_index(drop=True)                           

        df_punidas['cnpj'] = df_punidas['cnpj'].astype('int64')
        df_punidas['cnpj'] = df_punidas['cnpj'].astype('str')  

        df_punidas['cnpj'] = (df_punidas['cnpj'].str.rjust(14,"0"))       

        df_punidas = (df_punidas[['cnpj']]
                    .drop_duplicates(subset='cnpj')
                    .reset_index(drop=True)
                    .assign(classe = 'Empresa Punida'))
        
        return df_punidas

    # Entidades sem Fins Lucrativos Impedidas
    def tratar_arquivo_cepim(self, df_sem_fin_luc:pd.DataFrame):

        df_sem_fin_luc['MOTIVO DO IMPEDIMENTO'].unique()

        df_sem_fin_luc = (df_sem_fin_luc
                        .rename(columns={'CNPJ ENTIDADE':'cnpj'}))

        df_sem_fin_luc = df_sem_fin_luc.assign(cnpj = df_sem_fin_luc['cnpj'].astype(str))

        df_sem_fin_luc['cnpj'] = (df_sem_fin_luc['cnpj']
                                .replace(to_replace='\\.', value='', regex=True)
                                .replace(to_replace='-', value='', regex=True)
                                .replace(to_replace='\/', value='', regex=True))

        df_sem_fin_luc = df_sem_fin_luc.dropna(subset = 'cnpj').reset_index(drop=True)                           

        df_sem_fin_luc['cnpj'] = df_sem_fin_luc['cnpj'].astype('int64')
        df_sem_fin_luc['cnpj'] = df_sem_fin_luc['cnpj'].astype('str')  

        df_sem_fin_luc['cnpj'] = (df_sem_fin_luc['cnpj'].str.rjust(14,"0"))       

        df_sem_fin_luc = (df_sem_fin_luc[['cnpj']]
                        .drop_duplicates(subset='cnpj')
                        .reset_index(drop=True)
                        .assign(classe = 'Empresa Sem Fins Lucrativos Punida'))
        
        return df_sem_fin_luc
    
    # Executar tratamento para todos os grupos 
    def executar_tratamento_arquivos(self, 
                                     df_inid_arg:pd.DataFrame, 
                                     df_punidas_arg:pd.DataFrame, 
                                     df_sem_fin_luc_arg:pd.DataFrame, 
                                     return_df = False, 
                                     save_xlsx = True, 
                                     path_to_save = None):

        df_inid_tratado = self.tratar_arquivo_ceis(df_inid_arg)
        df_punidas_tratado = self.tratar_arquivo_cnep(df_punidas_arg)
        df_sem_fin_luc_tratado = self.tratar_arquivo_cepim(df_sem_fin_luc_arg)

        df_empresas_problemas = (pd.concat([df_inid_tratado, 
                                            df_punidas_tratado, 
                                            df_sem_fin_luc_tratado], ignore_index=True)
                                .drop_duplicates(subset='cnpj')
                                .reset_index(drop=True))
        
        if return_df is True:

            return df_empresas_problemas
        
        if save_xlsx is True and path_to_save is None:

            df_empresas_problemas.to_excel('empresas_punidas.xlsx', index=False)

            print("Arquivo 'empresas_punidas.xlsx' gerado com sucesso!")

        elif save_xlsx is True and path_to_save is not None:

            df_empresas_problemas.to_excel(os.path.join(path_to_save, 'empresas_punidas.xlsx'), index=False)

            print("Arquivo 'empresas_punidas.xlsx' gerado com sucesso na pasta solicitada!")

        elif save_xlsx is False and path_to_save is not None:

            print("Use 'save_xlsx = True' para salvar o arquivo no diretório escolhido.")

        elif save_xlsx is False and path_to_save is None and return_df is False:

            print("Use 'save_xlsx = True' para salvar o arquivo ou 'return_df = True' para obter o dataframe.")
