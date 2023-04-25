import pandas as pd
from sklearn.model_selection import train_test_split
from googletrans import Translator
import csv

# Função para tradução 
def translate_text(text, src_lang='en', dest_lang='pt'): 
    translator = Translator() 
    translation = translator.translate(text, src=src_lang, dest=dest_lang) 
    return translation.text 

#with open('TwetsChatGptTraduzido.csv', mode='w', newline='') as arquivo_csv:
    
    # cria um objeto writer da classe csv.writer
    #escritor_csv = csv.writer(arquivo_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    # escreve cada string da lista no arquivo CSV usando o método writerow()
    #data = pd.read_csv("DataSet.csv", nrows=200)
    #traducao = translate_text(data['Tweet'])
    #for string in traducao:
    #    escritor_csv.writerow([string])
        
# fecha o arquivo CSV
#arquivo_csv.close()

data = pd.read_csv("DataSet.csv")
traducao = translate_text(data['Tweet'])
print(traducao)