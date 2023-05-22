# NLP_Tweets_ChatGpt
 Analisador de sentimentos relacionados ao ChatGpt

## Descrição dos Scripts

1. **Translator.py**: Este script lê o arquivo de dados "DataSet.csv" e traduz cada tweet do inglês para o português. Devido ao limite do Google Translator, só pode fazer 1000 traduções por hora. As traduções são armazenadas no banco de dados SQLite para manter o rastreamento de quais tweets já foram traduzidos. Caso a tradução seja interrompida, o script pode continuar de onde parou, evitando retraduções.

2. **GetFileTranslated.py**: Este script recupera as traduções armazenadas no banco de dados SQLite e as salva em um arquivo CSV "ApenasTweets_PT.csv".

3. **ChatGPT.py**: Este script lê os tweets em inglês ("ApenasTweets.csv") e os tweets traduzidos em português ("ApenasTweets_PT.csv"), limpa e pré-processa os tweets, e então aplica a análise de sentimentos usando o pacote Vader do NLTK. 

## Como utilizar

1. Execute o script **Translator.py** para traduzir os tweets e salvar as traduções no banco de dados SQLite.

2. Execute o script **GetFileTranslated.py** para recuperar as traduções do banco de dados SQLite e salvar os tweets traduzidos em um arquivo CSV.

3. Execute o script **ChatGPT.py** para analisar o sentimento dos tweets em inglês e dos tweets traduzidos em português.
