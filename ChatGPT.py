import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
nltk.download("vader_lexicon")
nltk.download('punkt')
nltk.download('stopwords')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import sqlite3

# Cria conexão com o banco de dados SQLite
conn = sqlite3.connect('tweets.db')
cur = conn.cursor()

analyzer = SentimentIntensityAnalyzer()

def get_preprocess_tweet(lang):
    def preprocess_tweet(text):
        # Limpeza: Remover menções, URLs, números e caracteres especiais
        text = re.sub(r"@[A-Za-z0-9_]+", "", text)  # Remove menções
        text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)  # Remove URLs
        text = re.sub(r'\d+', '', text)  # Remove números
        text = re.sub(r'\W', ' ', text)  # Remove caracteres especiais
        
        # Tokenização
        tokens = word_tokenize(text)
        
        # Remoção de stopwords
        stop_words = set(stopwords.words(lang))
        tokens = [token for token in tokens if token not in stop_words]
        
        return " ".join(tokens)
    return preprocess_tweet

def vader_sentiment_result(sent):
    scores = analyzer.polarity_scores(sent)
    if scores["neg"] > scores["pos"]:
        return 0

    return 1

# def test(dataset):
#     for i, train_set in enumerate(dataset):
#         print(train_set)
#         # sentiment_train = vader_sentiment_result(train_set)
#         # cur.execute("UPDATE tweets SET sentiment_train_"+lang+" = "+sentiment_train+" where id = "+train_set["id"].to_string())

def analyze_sentiment():
    langs = ["english", "portuguese"]
    columns = ["Tweet", "TweetTranslated"]

    # Busca todos os dados da tabela 'tweets'
    cur.execute("SELECT id, Tweet, TweetTranslated  FROM tweets order by id")
    data = cur.fetchall()
    dataset = pd.DataFrame(data, columns=["id", columns[0], columns[1]])
    dataset = dataset.set_index('id')

    for i, lang in enumerate(langs):
        column_name = columns[i]

        # Pré-processar os tweets
        dataset[column_name] = dataset[column_name].apply(get_preprocess_tweet(lang))
        
    for i in dataset[0:4999].index:
        sentiment_portuguese = vader_sentiment_result(dataset.Tweet[i])
        sentiment_english = vader_sentiment_result(dataset.TweetTranslated[i])
        query = """UPDATE tweets SET sentiment_portuguese = ?,  sentiment_english = ? where id = ?"""
        cur.execute(query, (sentiment_portuguese, sentiment_english, i))
    
    for i in dataset[5001:7001].index:
        sentiment_portuguese = vader_sentiment_result(dataset.Tweet[i])
        sentiment_english = vader_sentiment_result(dataset.TweetTranslated[i])
        query = """UPDATE tweets SET sentiment_portuguese = ?,  sentiment_english = ? where id = ?"""
        cur.execute(query, (sentiment_portuguese, sentiment_english, i))

    conn.commit()

def analyze_sentiment_and_save_csv():
    langs = ["english", "portuguese"]
    columns = ["Tweet", "TweetTranslated"]

    for i, lang in enumerate(langs):
        column_name = columns[i]

        # Busca todos os dados da tabela 'tweets'
        cur.execute("SELECT id, "+column_name+",  FROM tweets order by id")
        data = cur.fetchall()
        dataset = pd.DataFrame(data, columns=["id", column_name])

        # Pré-processar os tweets
        dataset[column_name] = dataset[column_name].apply(get_preprocess_tweet(lang))

        train_set = dataset[0:4999]
        valid_set = dataset[5001:7001]

        train_set[column_name].apply(vader_sentiment_result)
        valid_set[column_name].apply(vader_sentiment_result)
        
        file_name = "ApenasTweets_"+lang+".csv"

        # Salvar train_set em um arquivo CSV
        train_set.to_csv(file_name + '_train.csv', index=False)

        # Salvar valid_set em um arquivo CSV
        valid_set.to_csv(file_name + '_valid.csv', index=False)

analyze_sentiment()
