import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
#file = open("tweets_spanish.txt", "r")
text = "Hey guys. This is Sun's fan and I welcome you to this episode of Dota Moments of the Week."

lista_tokenizada = word_tokenize(text, language="english")


phrases = ["Hola, amigo",
"Hola, enemigo"]

vect = CountVectorizer()
vect.fit(phrases)

print("Tamaño del vocabulario: {}".format(len(vect.vocabulary_)))
print("Contenido: {}".format(vect.vocabulary_))

bag_of_words = vect.transform(phrases).toarray()
print("Bag of words: {}".format(bag_of_words))