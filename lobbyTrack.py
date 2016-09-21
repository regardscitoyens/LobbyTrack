#!coding: utf-8

import nltk
from nltk import ngrams

# Variables
site = "nosdeputes.fr"
x = 5 # Nombre de mots par n-grams


f = open('example/document_lobby_example.txt')
raw = f.read()

# Retirer les retours chariots
raw = ''.join(raw.splitlines())

# Constuire des N-grams
# http://stackoverflow.com/questions/17531684/n-grams-in-python-four-five-six-grams

xgrams = ngrams(raw.split(), x)
for grams in xgrams:
  print('- Traitement du xgram : '  + ' '.join(grams))


# https://www.nosdeputes.fr/recherche/loi+1948?format=csv
