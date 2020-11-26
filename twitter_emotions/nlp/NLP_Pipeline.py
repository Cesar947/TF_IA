import nltk
import re
from nltk.tokenize import sent_tokenize, word_tokenize, TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

class NlpPipeline:
    def __init__(self, file, test_data_file=None):
        self.file = file
        self.tweet_list = []
        self.tokenized_list = []
        self.tweet_valid_words = None
        self.tagged_words = None
        self.lemmatized_words = None
        self.vocabulary = {}
        self.words_keys_in_bag = None
        self.available_words = []
        self.bag_of_words = None

    def remove_url_mentions(self, tweet, train_bool):
        # Expresión regular para eliminar los urls
        url_pattern = r"(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"
        # Reemplazar el string utilizado para separar los tweets
        text = ""
        if(train_bool):
            tweet = tweet.replace("|%&|\n", "")
        # Eliminar los url's
        text = re.sub(url_pattern, "", tweet)
        # Eliminar los hashtags, menciones o palabras con ampersam
        text = re.sub(r"[@#&]+(\w+\s?)\s?","", text)
        
        # Eliminar emojis de tipo :palabra:
        text = re.sub(r"[:]+(\w+\s?)[:]?\s?","", text)

        # Eliminar caracteres que no sean palabras
        text = re.sub(r'\W+', " ", text)
        return text
    
    def pre_process(self):
        cont = False
        text = ""
       
        for line in self.file.readlines():
            if line.split() == []:
                continue
            if cont:
                if("|%&|" in line[-6:]):
                    text = self.remove_url_mentions(line, True)
                    cont = False
                self.tweet_list[-1] = self.tweet_list[-1] + " " + text
            else:
                text = self.remove_url_mentions(line, True)
                self.tweet_list.append(text)
                if("|%&|" in line[-6:]):
                    continue
                else:
                    cont = True
        self.file.close()

    def tokenize_single_tweet(self, tweet, tokenizer):
        return tokenizer.tokenize(tweet)

    def tokenize(self):
        tokenizer = TweetTokenizer(strip_handles=True, reduce_len=True)
        for tweet in self.tweet_list:
            self.tokenized_list.append(self.tokenize_single_tweet(tweet,tokenizer))

    def remove_stop_words_single_tweet(self, tokens, stop_words):
        list_valid = []
        for token in tokens:
            if token not in stop_words:
                list_valid.append(token)
        return list_valid

    def remove_stop_words(self):
        self.tweet_valid_words = [[] for _ in range(len(self.tokenized_list))]
        stop_words = set(stopwords.words("english"))
        i = 0
        for tweet_tokens in self.tokenized_list:
            self.tweet_valid_words[i] = self.remove_stop_words_single_tweet(tweet_tokens, stop_words)
            i += 1

    def pos_tag(self):
        self.tagged_words = []
        for tweet in self.tweet_valid_words:
            self.tagged_words.append(nltk.pos_tag(tweet))

    def get_wordnet_pos(self, tag: str):
        if tag.startswith('J'):
            return wordnet.ADJ
        elif tag.startswith('V'):
            return wordnet.VERB
        elif tag.startswith('N'): 
            return wordnet.NOUN 
        elif tag.startswith('R'):
            return wordnet.ADV
        else:
            return None
    
    def lemmatize_single_tweet(self, tweet, lemmatizer):
        
        lema_list = []
        for word, pos_tag in tweet:
                pos = self.get_wordnet_pos(pos_tag)
                if pos is None:
                    lema_list.append(lemmatizer.lemmatize(word))
                else:
                    lema_list.append(lemmatizer.lemmatize(word, pos))
        return lema_list
        
    def lemmatize(self):
        lemmatizer = WordNetLemmatizer()
        self.lemmatized_words = [[] for _ in range(len(self.tagged_words))]
        i = 0
        for tweet in self.tagged_words:
            self.lemmatized_words[i] = self.lemmatize_single_tweet(tweet, lemmatizer)
            i += 1

    #Convertir a Bag of Words
    def vectorize(self):
        count_vec = CountVectorizer()
        tweets = []
        for list_strings in self.lemmatized_words:
            tweets.append(' '.join(list_strings))
        count_vec.fit(tweets)

        self.vocabulary = {value: key for key, value in count_vec.vocabulary_.items()}


        aux_bag = count_vec.transform(tweets).toarray()
        dict_aux = {}
        
        for i, words in enumerate(aux_bag):
            for word_number, frecuency in enumerate(words):
                if i == 0:
                    dict_aux[word_number] = frecuency
                elif frecuency != 0:
                    dict_aux[word_number] += frecuency
        
        self.words_keys_in_bag = sorted(dict_aux, key=dict_aux.get, reverse=True)[:3000]

        aux_vocabulary = {} 
        for key in self.words_keys_in_bag:
            aux_vocabulary[key] = self.vocabulary[key]
        self.vocabulary = aux_vocabulary

        bag_of_words_filtered = [[] for _ in range(len(aux_bag))]
        i = 0
        for words in aux_bag:
            for key in self.words_keys_in_bag:
                bag_of_words_filtered[i].append(words[key])
            i += 1
        self.bag_of_words = np.array(bag_of_words_filtered)
        print("### BAG OF WORDS ###")
        print(self.bag_of_words)
        print(f"Rows: {len(self.bag_of_words)}, Columns: {len(self.bag_of_words[0])}")

       

    def run_pipeline(self):
        self.pre_process()
        self.tokenize()
        self.remove_stop_words()
        self.pos_tag()
        self.lemmatize()
        self.vectorize()

    def test_tweet_vectorization(self, tweet):

        # Pipeline para un solo tweet (El que será procesado en la app ya entrenada)

        clean_tweet = self.remove_url_mentions(tweet, False)

        tokenizer = TweetTokenizer(strip_handles=True, reduce_len=True)
        tokenized = self.tokenize_single_tweet(clean_tweet, tokenizer)

        stop_words = set(stopwords.words("english"))
        without_stop_words = self.remove_stop_words_single_tweet(tokenized, stop_words)

        pos_tagged = nltk.pos_tag(without_stop_words)

        lemmatizer = WordNetLemmatizer()
        lema_list = self.lemmatize_single_tweet(pos_tagged, lemmatizer)

        # Cuando el tweet esté tokenizado
        # Se procederá a construir su matriz de frecuencia
        # de acuerdo al vocabulario de entrenamiento
        # Obtenemos el tamaño de la cantidad de keys de palabras disponibles
        ## En este caso son 1000
        # E inicializamos el vector con 0's
        n = len(self.words_keys_in_bag)
        vector = [0 for _ in range(n)]

        # Por cada palabra en la lista
        for word in lema_list:
            i = 0
            # Iterando en la lista de keys (Debe iterar ordenadamente)
            for key in self.words_keys_in_bag:
                # Si la palabra es igual a la palabra del vocabulario
                if word == self.vocabulary[key]:
                    # Aumenta en 1 al vector en la posición i que llega hasta 1000 (Porque son 1000 palabras en el vocabulario)
                    vector[i] += 1
                i += 1

        return np.array(vector)


# test = "I wanna say thanks to all the supporter this Season! :heart:\n"+\
# "You guys motivated me a lot to improve everyday and you guys know how ambitious"+\
# " I am so it’s always tough for me to lose this important games...\nThere is still"+\
# " worlds left and I will be ready for that!\nDon’t count us out:wink:"
# vector = pipeline.test_tweet_vectorization(test)
# c = 0
# for v in vector:
#     if v == 1:
#         c += 1
# print(f"Tiene {c} coincidencias con el vocabulario")
