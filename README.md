# Coleta, Tratamento e Classificação de Notas Fiscais e Empresas Punidas

## Projeto desenvolvido para o Mestrado em Ciência da Computação pela Universidade Federal da Bahia (UBFA)

## Visão Geral

Este repositório automatiza o download, extração, tratamento e classificação de dados de Notas Fiscais Eletrônicas (NFe) e de empresas punidas (CEIS, CNEP, CEPIM) a partir de fontes públicas. Além disso, inclui notebooks para treinamento e avaliação de modelos de linguagem (LLMs) para classificação desses dados.

---

## Estrutura dos Arquivos

### 1. **Download_Extracao_NFe.py**

- **O que faz:**  
  Baixa e extrai arquivos de Notas Fiscais Eletrônicas (NFe) de um mês/ano específico do Portal da Transparência.
- **Como funciona:**  
  - Recebe um parâmetro `ano_mes` (ex: "202306").
  - Baixa o arquivo ZIP correspondente.
  - Extrai o conteúdo para uma pasta temporária.
  - Move os arquivos extraídos para uma pasta do ano correspondente.
  - Remove arquivos temporários após a extração.
- **Uso:**  
  Instancie a classe `Download_Extracao_NFe("202306")` para baixar e extrair os dados de junho de 2023.

---

### 2. **Download_Empresas_Punidas.py**

- **O que faz:**  
  Baixa e extrai os arquivos mais recentes das listas de empresas punidas (CEIS, CNEP, CEPIM) dos últimos 15 dias.
- **Como funciona:**  
  - Gera um intervalo de datas dos últimos 15 dias.
  - Para cada categoria (CEIS, CNEP, CEPIM), tenta baixar o arquivo mais recente disponível.
  - Extrai o conteúdo de cada ZIP para uma pasta específica da categoria.
  - Remove arquivos temporários após a extração.
- **Uso:**  
  Instancie a classe `Download_Extracao_Empresas_Punidas()` para baixar e extrair os dados mais recentes de cada lista.

---

### 3. **Tratamento_Empresas_Punidas.py**

- **O que faz:**  
  Realiza o tratamento dos dados extraídos das listas de empresas punidas, padronizando e consolidando as informações.
- **Como funciona:**  
  - Lê os arquivos extraídos das pastas CEIS, CNEP e CEPIM.
  - Realiza limpeza, padronização e consolidação dos dados.
  - Permite salvar o resultado em Excel ou retornar como DataFrame.
- **Uso:**  
  Instancie a classe `Tratamento_Empresas_Punidas` e utilize seus métodos para tratar e salvar os dados.

---

### 4. **Tratamento_NFe.py**

- **O que faz:**  
  Realiza o tratamento dos dados de Notas Fiscais Eletrônicas, cruzando com a lista de empresas punidas.
- **Como funciona:**  
  - Lê os arquivos de NFe extraídos para um determinado ano.
  - Realiza limpeza, padronização e cruzamento com a lista de empresas punidas.
  - Permite salvar o resultado em formato Parquet ou retornar como DataFrame.
- **Uso:**  
  Instancie a classe `Tratamento_NFe` e utilize seus métodos para tratar e salvar os dados.

---

### 5. **Execucao_Coleta_Tratamento_Dados.py**

- **O que faz:**  
  Orquestra todo o processo de download, extração e tratamento dos dados de empresas punidas e NFe.
- **Como funciona:**  
  - Baixa e trata os dados das empresas punidas.
  - Baixa e trata os dados de NFe para todos os meses de um ano ou para um mês específico.
  - Salva os resultados tratados em arquivos prontos para uso em análises ou modelos.
- **Uso:**  
  Execute o script diretamente ou chame a função `Execucao_Coleta_Tratamento_Dados(ano_selecionado="2025", ano_mes=None)`.

---

### 6. **Execucao_Modelo_Treinado_HF.py**

- **O que faz:**  
  Executa o modelo de classificação de texto desenvolvido neste trabalho e disponível no Hugging Face para identificar padrões em textos de NFe.
- **Como funciona:**  
  - Carrega o modelo e o tokenizer do Hugging Face.
  - Usa o pipeline de classificação para prever a classe de um texto de exemplo.
- **Uso:**  
  Execute o script para testar a classificação de um texto de NFe usando o modelo treinado.

---

### 7. **Model_FewShot.ipynb**

- **O que faz:**  
  Notebook para avaliação de modelos LLMs usando abordagem few-shot para classificação de textos de NFe.
- **Como funciona:**  
  - Carrega e prepara o dataset de NFe.
  - Cria amostras balanceadas para treino e teste.
  - Gera prompts few-shot para avaliação de LLMs.
  - Mede métricas como acurácia, precisão, recall, F1 e custo de erros.
- **Uso:**  
  Execute célula a célula para treinar, avaliar e analisar o desempenho de LLMs em classificação de NFe.

---

### 8. **Model_LLM_Finetuning.ipynb**

- **O que faz:**  
  Notebook para fine-tuning de modelos LLMs em dados de NFe.
- **Como funciona:**  
  - Prepara os dados para fine-tuning.
  - Configura e executa o treinamento do modelo.
  - Avalia o modelo ajustado.
- **Uso:**  
  Execute célula a célula para treinar, avaliar e analisar o desempenho de LLMs em classificação de NFe.

---

### 9. **Model_ZeroShot.ipynb**

- **O que faz:**  
  Notebook para avaliação de modelos LLMs em zero-shot para classificação de textos de NFe.
- **Como funciona:**  
  - Prepara o dataset.
  - Gera prompts zero-shot.
  - Avalia o desempenho do modelo sem exemplos de treino.
- **Uso:**  
  Execute célula a célula para treinar, avaliar e analisar o desempenho de LLMs em classificação de NFe.

---

### 10. **requirements.txt**

- **O que faz:**  
  Lista das dependências necessárias para rodar o projeto.

---

## Fluxo de Execução Sugerido

1. **Coleta e Tratamento dos Dados:**
   - Execute `Execucao_Coleta_Tratamento_Dados.py` para baixar, extrair e tratar todos os dados necessários.
2. **Classificação com Modelo Treinado:**
   - Use `Execucao_Modelo_Treinado_HF.py` para testar a classificação de textos com um modelo já treinado.
3. **Treinamento e Avaliação de Modelos:**
   - Use os notebooks (`Model_FewShot.ipynb`, `Model_LLM_Finetuning.ipynb`, `Model_ZeroShot.ipynb`) para treinar, ajustar e avaliar novos modelos LLMs.

---

## Observações

- Os scripts de download e tratamento são independentes, mas o tratamento depende dos arquivos extraídos previamente.
- Os notebooks são voltados para experimentação e avaliação de modelos de linguagem.
- Certifique-se de instalar todas as dependências do `requirements.txt` antes de executar os scripts e notebooks.

