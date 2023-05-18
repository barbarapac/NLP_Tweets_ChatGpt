import pandas as pd
from sklearn.model_selection import train_test_split
from googletrans import Translator
import csv
import nltk
nltk.download("vader_lexicon")
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import csv

# Função para tradução 
#def translate_text(text, src_lang='en', dest_lang='pt'): 
#    translator = Translator() 
#    translation = translator.translate(text, src=src_lang, dest=dest_lang) 
#    return translation.text 

# Funcao que cria um novo arquivo CSV com apenas 10000 TWEETS
#with open('ApenasTweets.csv', mode='w', newline='') as arquivo_csv:
#    escritor_csv = csv.writer(arquivo_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)    
#    data = pd.read_csv("ChatGPT.csv", nrows=10000, low_memory=False)
#    dw = csv.DictWriter(arquivo_csv, delimiter=',',fieldnames=headerList)
#    dw.writeheader()
#    for string in data['Tweet']:
#       escritor_csv.writerow([string])
        
dataset = pd.read_csv("ApenasTweets.csv")
# 2) Divida os dados em conjuntos de treinamento/validacao/teste.
train_set = dataset[0:5000]
valid_set = dataset[5001:7000]
test_set  = dataset[7001:10000]

# Cria um objeto Vader para usar a funcao preditora. (vader_sentiment_result())
#print(train_set["Tweet"])
analyzer = SentimentIntensityAnalyzer()

#  Funcao retorna zero para sentimentos negativos (se a pontuacao negativa de Vader for maior que positiva) ou um caso o sentimento seja positivo
def vader_sentiment_result(sent):
    scores = analyzer.polarity_scores(sent)
    
    if scores["neg"] > scores["pos"]:
        return 0

    return 1

# Em seguida, utilizamos a funcao para prever os sentimentos de cada linha no conjunto de treinamento e validacao e colocar os resultados em uma nova coluna chamada vader_result
train_set["sentimento"] = train_set["Tweet"].apply(lambda x: vader_sentiment_result(x))
valid_set["sentimento"] = valid_set["Tweet"].apply(lambda x: vader_sentiment_result(x))

print(train_set)
print(valid_set)