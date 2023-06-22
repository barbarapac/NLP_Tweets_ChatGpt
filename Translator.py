import pandas as pd
import time
import sqlite3
from googletrans import Translator

# Carrega o dataset
dataset = pd.read_csv("DataSet.csv", index_col=False, low_memory=False)

# Cria um objeto do tradutor
translator = Translator()

# Função para traduzir o texto
def translate_text(text):
    # Traduz o texto para o português
    # print("Traduzindo: " + text)
    translation = translator.translate(text, src='en', dest='pt')
    # print("Tradução: " + translation.text)
    return translation.text

# Define o limite de traduções por hora
limit = 1000

# Cria conexão com o banco de dados SQLite
conn = sqlite3.connect('tweets.db')
cur = conn.cursor()

# Cria a tabela 'tweets' no SQLite se ela ainda não existir
cur.execute('''
    CREATE TABLE IF NOT EXISTS tweets (
        id ROWID,
        Date TEXT,
        Tweet TEXT,
        TweetTranslated TEXT,
        Url TEXT,
        User TEXT,
        UserCreated TEXT,
        UserVerified TEXT,
        UserFollowers INTEGER,
        UserFriends INTEGER,
        Retweets INTEGER,
        Likes INTEGER,
        Location TEXT,
        Description TEXT
    )
''')

for index, row in dataset.iterrows():
    # Verifica se a linha já foi traduzida
    cur.execute("SELECT * FROM tweets WHERE Date = ?", (row['Date'],))
    data = cur.fetchone()
    
    # Se a linha ainda não foi traduzida, traduz e salva no SQLite
    if data is None:
        print("Traduzindo linha " + str(index+1) + " de " + str(len(dataset)))
        row['TweetTranslated'] = translate_text(str(row['Tweet']))
        pd.DataFrame(row).T.to_sql('tweets', conn, if_exists='append', index=False)
        
        # Espera 1 hora após atingir o limite de traduções por hora
        # if (index+1) % limit == 0:
        #     print("Esperando 1 hora antes de continuar as traduções...")
        #     time.sleep(60*60)

# Fecha a conexão com o banco de dados SQLite
conn.close()
