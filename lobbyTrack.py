#!coding: utf-8

import requests
import nltk
from nltk import ngrams
import re
from collections import Counter
import argparse
from os.path import expanduser
import os
import hashlib
import pickle

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

def computeMD5hash(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()

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

    hash = computeMD5hash(args.file)
    path = expanduser("~")+"/.lobbyTrack/"+hash
    if not os.path.exists(path):
        os.makedirs(path)

    raw_string = getStringFromFile(args.file)
    xgrams = getNGrams(raw_string, args.grams)
    counter = Counter()
    gram_hash_list = []
    for gram in xgrams:
        # On charge la structure de données si elle existe
        if os.path.exists(path+'/counter.pickle'):
            with open(path+'/counter.pickle', 'rb') as f:
                counter = pickle.load(f)
        if os.path.exists(path+'/gram_hash_list.pickle'):
            with open(path+'/gram_hash_list.pickle', 'rb') as f:
                gram_hash_list = pickle.load(f)

        # Si la requête n'a pas déjà été faite alors on la fait
        str_gram = ' '.join(gram)
        gram_hash = computeMD5hash(str_gram)
        if (gram_hash not in gram_hash_list):
            counter = getCounterByNGram(str_gram, counter, args.site)

        # On écrit la structure de données
        with open(path+'/counter.pickle', 'wb') as f:
            pickle.dump(counter, f)
        with open(path+'/gram_hash_list.pickle', 'wb') as f:
            gram_hash_list.append(gram_hash)
            pickle.dump(gram_hash_list, f)
    print('------')
    print(Counter(counter).most_common(3))
