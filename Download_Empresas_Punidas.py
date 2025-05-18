


import requests as rq 
import zipfile
import os
import shutil
import pandas as pd
import datetime
from glob import glob

###################################################################
#### Class --------------------------------------------------------
###################################################################

class Download_Extracao_Empresas_Punidas:

    '''
    Chame a classe para obter o arquivo mais recente de cada entidade.

    Exemplo: Download_Extracao_Empresas_Punidas()
    '''

    def __init__(self):

        self.baixar_todos_zips()

        self.descompactar_todos_zips()

    # Intervalo de datas
    def gerar_intervalo_datas(self):

        dt_0 = datetime.date.today()

        dt_d15 = dt_0 - datetime.timedelta(days = 15)

        list_datas = pd.date_range(start = dt_d15, end = dt_0).strftime("%Y%m%d").tolist()

        return list_datas

    # Empresas Inidôneas e Suspensas
    def baixar_ceis_zip(self, data:str):

        '''data: data no formato YMD. Exemplo de uso: "20250516".'''

        rq_ceis = rq.get(f"https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/ceis/{data}_CEIS.zip")

        if rq_ceis.status_code == 200:

            with open(f"{data}_CEIS.zip", 'wb') as f:

                f.write(rq_ceis.content)

            print(f'Arquivo zip CEIS para {data} baixado com sucesso.')

        else:
            
            print(f'Erro ao baixar arquivo CEIS para {data}: Status {rq_ceis.status_code}')

        return rq_ceis.status_code

    # Empresas Punidas
    def baixar_cnep_zip(self, data:str):

        '''data: data no formato YMD. Exemplo de uso: "20250516".'''

        rq_cnep = rq.get(f"https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/cnep/{data}_CNEP.zip")

        if rq_cnep.status_code == 200:

            with open(f"{data}_CNEP.zip", 'wb') as f:

                f.write(rq_cnep.content)

            print(f'Arquivo zip CNEP para {data} baixado com sucesso.')

        else:
            
            print(f'Erro ao baixar arquivo CNEP para {data}: Status {rq_cnep.status_code}')

        return rq_cnep.status_code

    # Entidades sem Fins Lucrativos Impedidas
    def baixar_cepim_zip(self, data:str):

        '''data: data no formato YMD. Exemplo de uso: "20250516".'''

        rq_cepim = rq.get(f"https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/cepim/{data}_CEPIM.zip")

        if rq_cepim.status_code == 200:

            with open(f"{data}_CEPIM.zip", 'wb') as f:

                f.write(rq_cepim.content)

            print(f'Arquivo zip CEPIM para {data} baixado com sucesso.')

        else:
            
            print(f'Erro ao baixar arquivo CEPIM para {data}: Status {rq_cepim.status_code}')

        return rq_cepim.status_code

    # Descompactar arquivo no diretorio
    def descompactar_zip(self, nm_file:str, categoria:str):

        '''
           * data: data no formato YMD. Exemplo de uso: "20250516".
           * arquivo: use somente "CEPIM", "CNEP" ou "CEIS".
        '''

        pasta_extracao = f'extracao_temp_{categoria}'

        with zipfile.ZipFile(nm_file, 'r') as zip_ref:

            zip_ref.extractall(pasta_extracao)

        if not os.path.exists(categoria):

            os.makedirs(categoria)

            print(f'Pasta "{categoria}" criada com sucesso.')

        for file in os.listdir(pasta_extracao):

            caminho_origem = os.path.join(pasta_extracao, file)

            caminho_destino = os.path.join(categoria, file)

            shutil.move(caminho_origem, caminho_destino)

        print(f'Arquivos movidos para pasta "{categoria}".')

        os.remove(nm_file)

        shutil.rmtree(pasta_extracao)

    def baixar_todos_zips(self):

        datas = self.gerar_intervalo_datas()

        # Execução para CNEP
        try:

            for d in reversed(datas):   

                if self.baixar_cnep_zip(d) == 200:

                    break                     
            
            else:

                print("Nenhum arquivo disponível para os últimos 15 dias.")

        except Exception as error:

            print("Problema na execução para o CNEP. Log de erro:\n", error)

        # Execução para CEIS
        try:

            for d in reversed(datas):   

                if self.baixar_ceis_zip(d) == 200:

                    break                     
            
            else:

                print("Nenhum arquivo disponível para os últimos 15 dias.")

        except Exception as error:

            print("Problema na execução para o CEIS. Log de erro:\n", error)

        # Execução para CEPIM
        try:

            for d in reversed(datas):   

                if self.baixar_cepim_zip(d) == 200:

                    break                     
            
            else:

                print("Nenhum arquivo disponível para os últimos 15 dias.")

        except Exception as error:

            print("Problema na execução para o CEIS. Log de erro:\n", error)

    def descompactar_todos_zips(self):

        nm_file_ceis = glob("*_CEIS.zip")[0]
        nm_file_cnep = glob("*_CNEP.zip")[0]
        nm_file_cepim = glob("*_CEPIM.zip")[0]

        self.descompactar_zip(nm_file_ceis, "CEIS")
        self.descompactar_zip(nm_file_cnep, "CNEP")
        self.descompactar_zip(nm_file_cepim, "CEPIM")


###################################################################
#### Execução -----------------------------------------------------
###################################################################

# Exemplo
Download_Extracao_Empresas_Punidas()