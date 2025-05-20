


import requests as rq 
import zipfile
import os
import shutil

###################################################################
#### Class --------------------------------------------------------
###################################################################

class Download_Extracao_NFe:

    '''
    Informe o ano e o mês que deseja fazer o download. Use o formato str. Exemplo "202306".

    Exemplo de uso: Download_Extracao_NFe("202306")
    '''

    def __init__(self, ano_mes:str):

        self.ano_mes = ano_mes
        self.baixar_nfe_zip(self.ano_mes)
        self.descompactar_nfe_zip(self.ano_mes)

    def baixar_nfe_zip(self, ano_mes:str):

        '''ano_mes: ano e mês do arquivo. Exemplo de uso: "202412".'''

        rq_nfe = rq.get(f"https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/nfe/{ano_mes}_NFe.zip")

        if rq_nfe.status_code == 200:

            with open(f"{ano_mes}_NFe.zip", 'wb') as f:

                f.write(rq_nfe.content)

            print(f'Arquivo zip {ano_mes} baixado com sucesso.')

        else:
            
            print(f'Erro ao baixar arquivo {ano_mes}: Status {rq_nfe.status_code}')

    def descompactar_nfe_zip(self, ano_mes:str):

        '''ano_mes: ano e mês do arquivo. Exemplo de uso: "202412".'''

        pasta_extracao = f'extracao_temp_{ano_mes}'

        nome_arquivo_zip = ano_mes + "_NFe.zip"

        with zipfile.ZipFile(nome_arquivo_zip, 'r') as zip_ref:

            zip_ref.extractall(pasta_extracao)

        pasta_ano = ano_mes[:4]

        if not os.path.exists(pasta_ano):

            os.makedirs(pasta_ano)

            print(f'Pasta "{pasta_ano}" criada com sucesso.')

        for arquivo in os.listdir(pasta_extracao):

            caminho_origem = os.path.join(pasta_extracao, arquivo)

            caminho_destino = os.path.join(pasta_ano, arquivo)

            shutil.move(caminho_origem, caminho_destino)

        print(f'Arquivos movidos para pasta "{pasta_ano}".')

        os.remove(nome_arquivo_zip)

        shutil.rmtree(pasta_extracao)
