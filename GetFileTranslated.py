import pandas as pd
import sqlite3

# Cria conexão com o banco de dados SQLite
conn = sqlite3.connect('tweets.db')
cur = conn.cursor()

# Busca todos os dados da tabela 'tweets'
cur.execute("SELECT Tweet FROM tweets")
data = cur.fetchall()

# Cria um DataFrame a partir dos dados
df = pd.DataFrame(data, columns=['Tweet'])

# Salva o DataFrame em um arquivo CSV
df.to_csv('ApenasTweets_PT.csv', index=False)

# Fecha a conexão com o banco de dados SQLite
conn.close()

print("Os dados foram salvos com sucesso em 'ApenasTweets_PT.csv'")
