import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
nltk.download("vader_lexicon")
nltk.download('punkt')
nltk.download('stopwords')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

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

def analyze_sentiment(file_name, lang):
    dataset = pd.read_csv(file_name)

    # Pré-processar os tweets
    dataset['Tweet'] = dataset['Tweet'].apply(get_preprocess_tweet(lang))

    train_set = dataset[0:5000]
    valid_set = dataset[5001:7000]

    train_set["sentimento"] = train_set["Tweet"].apply(lambda x: vader_sentiment_result(x))
    valid_set["sentimento"] = valid_set["Tweet"].apply(lambda x: vader_sentiment_result(x))

    print(train_set)
    print(valid_set)

analyze_sentiment("ApenasTweets.csv", "english")
analyze_sentiment("ApenasTweets_PT.csv", "portuguese")