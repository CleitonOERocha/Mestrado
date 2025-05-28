

from Download_Empresas_Punidas import Download_Extracao_Empresas_Punidas 
from Download_Extracao_NFe import Download_Extracao_NFe 
from Tratamento_Empresas_Punidas import Tratamento_Empresas_Punidas 
from Tratamento_NFe import Tratamento_NFe 

def Execucao_Coleta_Tratamento_Dados(ano_selecionado:str, ano_mes:str = None):

    '''
    <br />

    Função que realiza a coleta e tratamento dos dados de empresas e notas fiscais.
    O resultado final é o arquivo ".parquet" tratado pronto para uso nos códigos em Jupyter.

    <br />

    Argumentos:

    * ano_selecionado = Ano que deseja gerar o arquivo. Usar no formato str. Exemplo "2024", "2023", etc.

    <br />

    * ano_mes = Ano/Mês desejado para download. Por padrão, "ano_mes" está configurado
    para ser None, nesse caso, o código vai executar para todos os meses 
    do ano escolhido em "ano_selecionado". Caso "ano_mes" não seja None, 
    use o campo no formato str, por exemplo: "202503". 

    '''

    if len(ano_selecionado) != 4 or not ano_selecionado.isdigit():

        print("O ano selecionado deve ser uma string com 4 dígitos, ex.: '2025'")

    else:

        Download_Extracao_Empresas_Punidas()

        if ano_mes is None:

            print("Realizando download para todos os meses do ano.")
            
            lista_meses_ano = [f"{ano_selecionado}{mes:02d}" for mes in range(1, 13)]

            for i in lista_meses_ano:

                try:

                    Download_Extracao_NFe(i)

                except:

                    print("Download não concluído para o mês ", i)

        else:

            Download_Extracao_NFe(ano_mes)

        Tratamento_Empresas_Punidas(retornar_dataframe = False, 
                                    salvar_xlsx = True, 
                                    pasta_para_salvar = None)

        Tratamento_NFe(ano = ano_selecionado, 
                       arquivo_empresas = "empresas_punidas.xlsx", 
                       retornar_dataframe = False, 
                       save_parquet = True, 
                       pasta_para_salvar = None)
        
        print("Execução concluída!")
    

if __name__ == "__main__":

    Execucao_Coleta_Tratamento_Dados(ano_selecionado = "2025", ano_mes = None)