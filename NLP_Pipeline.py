import nltk
import re
from nltk.tokenize import sent_tokenize, word_tokenize, TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer

class NlpPipeline:
    def __init__(self):
        self.train_file = open("tweets_hashtag.txt", "r", encoding="utf8")
        self.tweet_list = []
        self.tokenized_list = []
        self.tweet_valid_words = None
        self.tagged_words = None
        self.lemmatized_words = None

    def remove_url_mentions(self, tweet):
        url_pattern = r"(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"
        text = tweet.replace("|%&|\n", "")
        text = re.sub(url_pattern, "", text)
        text = re.sub(r'\W+', " ", text)

        return text

    def pre_process(self):
        cont = False
        text = ""
       
        for line in self.train_file.readlines():
            if(line.split() == []):
                continue
            if(cont):
                if("|%&|" in line[-6:]):
                    text = self.remove_url_mentions(line)
                    cont = False
                self.tweet_list[-1] = self.tweet_list[-1] + " " + text
            else:
                text = self.remove_url_mentions(line)
                self.tweet_list.append(text)
                if("|%&|" in line[-6:]):
                    continue
                else:
                    cont = True
        self.train_file.close()

    def tokenize(self):
        tokenizer = TweetTokenizer(strip_handles=True, reduce_len=True)
        for tweet in self.tweet_list:
            self.tokenized_list.append(tokenizer.tokenize(tweet))


    def remove_stop_words(self):
        self.tweet_valid_words = [[] for _ in range(len(self.tokenized_list))]
        stop_words = set(stopwords.words("english"))
        i = 0
        for tweet_tokens in self.tokenized_list:
            for token in tweet_tokens:
                if token not in stop_words:
                    self.tweet_valid_words[i].append(token) 
            i += 1

    # def pos_tag(self):
    #     self.tagged_words = []

    #     for tweet in self.tweet_valid_words:
    #         self.tagged_words.append(nltk.pos_tag(tweet))

    
    def lemmatize(self):
        lemmatizer = WordNetLemmatizer()
        self.lemmatized_words = [[] for _ in range(len(self.tweet_valid_words))]
        i = 0
        for tweet in self.tweet_valid_words:
            for word in tweet:
                self.lemmatized_words[i].append(lemmatizer.lemmatize(word))
            i += 1

    #Convertir a Bag of Words
    def vectorize(self):
        pass

    def run_pipeline(self):
        self.pre_process()
        self.tokenize()
        self.remove_stop_words()
        #self.pos_tag()
        self.lemmatize()

pipeline = NlpPipeline()
pipeline.run_pipeline()

print(pipeline.lemmatized_words)
 

    