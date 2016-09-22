#!coding: utf-8

import requests
import nltk
from nltk import ngrams
import re
from collections import Counter

# Variables
site = "nosdeputes.fr"
x = 5 # Nombre de mots par n-grams

def getStringFromFile(filename):
    f = open(filename)
    raw = f.read()
    # Retirer les retours chariots
    raw = ''.join(raw.splitlines())
    return raw

# Constuire des N-grams
# http://stackoverflow.com/questions/17531684/n-grams-in-python-four-five-six-grams
def getNGrams(raw_string):
    xgrams = ngrams(raw_string.split(), x)
    return xgrams

def getCounterByNGram(gram, counter):
        str_gram = ' '.join(gram)
        print('- Traitement du xgram : '  + str_gram)
        # https://www.nosdeputes.fr/recherche/loi+1948?format=csv
        url = 'http://'+site+'/recherche/'+str_gram+'?format=csv'
        print('-- Url appelé : '+url)
        response = requests.get(url, timeout=3)
        print ('-- Code retour : ' +str(response.status_code))

        # Améliorer le résultat du contenu
        urls = re.findall(b'http://.*/csv', response.content)
        #print('-- urls :'+urls)
        for url in urls:
            url = url.decode("utf-8")
            counter[url] += 1
        return counter




#http://cocolulu.regardscitoyens.org/LobbyTrackBio/biodiversiteglobal/synthese.html


if __name__ == '__main__':
    raw_string = getStringFromFile('example/document_lobby_example.txt')
    xgrams = getNGrams(raw_string)
    counter = Counter()
    for gram in xgrams:
        counter = getCounterByNGram(gram, counter)

    print('------')
    print(Counter(counter).most_common(3))
