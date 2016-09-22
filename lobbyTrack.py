#!coding: utf-8

import requests
import nltk
from nltk import ngrams
import re
from collections import Counter
import argparse

def getStringFromFile(filename):
    f = open(filename)
    raw = f.read()
    # Retirer les retours chariots
    raw = ''.join(raw.splitlines())
    return raw

# Constuire des N-grams
# http://stackoverflow.com/questions/17531684/n-grams-in-python-four-five-six-grams
def getNGrams(raw_string, gram_nb):
    xgrams = ngrams(raw_string.split(), gram_nb)
    return xgrams

def getCounterByNGram(gram, counter, site):
        str_gram = ' '.join(gram)
        print('- Traitement du xgram : '  + str_gram)
        # https://www.nosdeputes.fr/recherche/loi+1948?format=csv
        url = 'http://'+site+'/recherche/'+str_gram+'?format=csv'
        print('-- Url appelé : '+url)
        response = getResponseFromRequest(url, 3)
        if not response:
            return counter

        print ('-- Code retour : ' +str(response.status_code))
        # Améliorer le résultat du contenu
        urls = re.findall(b'http://.*/csv', response.content)
        #print('-- urls :'+urls)
        for url in urls:
            url = url.decode("utf-8")
            counter[url] += 1
        return counter

def getResponseFromRequest(url, nbtries):
    try:
        return requests.get(url, timeout=1)
    except requests.exceptions.RequestException as e:
        if (nbtries > 1):
            getResponseFromRequest(url,nbtries-1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", help="nosdeputes.fr or nossenateurs.fr", default="nosdeputes.fr")
    parser.add_argument("--grams", help="grams", default=5)
    parser.add_argument("file", help="file to check")
    args = parser.parse_args()

    raw_string = getStringFromFile(args.file)
    xgrams = getNGrams(raw_string, args.grams)
    counter = Counter()
    for gram in xgrams:
        counter = getCounterByNGram(gram, counter, args.site)

    print('------')
    print(Counter(counter).most_common(3))
