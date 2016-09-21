#!coding: utf-8

import requests
import nltk
from nltk import ngrams
import re
from collections import Counter

# Variables
site = "nosdeputes.fr"
x = 5 # Nombre de mots par n-grams


f = open('example/document_lobby_example.txt')
raw = f.read()

# Retirer les retours chariots
raw = ''.join(raw.splitlines())

# Constuire des N-grams
# http://stackoverflow.com/questions/17531684/n-grams-in-python-four-five-six-grams
counter = Counter()
xgrams = ngrams(raw.split(), x)
for gram in xgrams:
    str_gram = ' '.join(gram)
    print('- Traitement du xgram : '  + str_gram)
    # https://www.nosdeputes.fr/recherche/loi+1948?format=csv
    url = 'http://'+site+'/recherche/'+str_gram+'?format=csv'
    print('-- Url appelé : '+url)
    response = requests.get(url)
    print ('-- Code retour : ' +str(response.status_code))

    # Améliorer le résultat du contenu
    urls = re.findall(b'http://.*/csv', response.content)
    #print('-- urls :'+urls)
    for url in urls:
        url = url.decode("utf-8")
        counter[url] += 1
    list = Counter(counter).most_common(3)
    print(list)

print('------')
print(Counter(counter).most_common(10))
