#!coding: utf-8

import sys
import re

ngram = 4

def file2array(file):
    txt = re.sub(u"[\?\+‑\.!,;–()'’-]", " ", file.read().decode('UTF-8'))
    txt = re.sub(u'’', '\'', txt)
    txt = re.sub('\n+', ' <br/> ', txt)
    txt = re.sub(u' *([«"»]) *', r' " ', txt)
    txt = re.sub('L(\d)', r'L \1', txt)
    return [mot for mot in re.split("\s+", txt) if mot]

def printHighlight(mots, match, withnbmots=""):
    html = ''
    nb = 0
    max = 0
    for i, mot in enumerate(mots):
        if match[i]:
            html += '<span class="highlight">'
            nb += 1
        else:
            html += '<span>';
            if nb > max:
                max = nb
            nb = 0
        html += mot
        html += ' </span>';
    html = '<p>'+re.sub('<br/>', '</p><p>', html)+'</p>'
    print(html.encode('UTF-8'))
    if (withnbmots):
        sys.stderr.write(str(max)+";"+withnbmots + "\n")

with open(sys.argv[1], 'r') as f:
    mots1 = file2array(f)

with open(sys.argv[2], 'r') as f:
    mots2 = file2array(f)

if len(sys.argv) > 3 :
    ngram = int(sys.argv[3])

match1 = [0] * len(mots1)
match2 = [0] * len(mots2)

for i in range(0, len(mots1) - ngram):
    for y in range(0, len(mots2) - ngram):
        if re.match(' '.join(mots1[i:i+ngram]), ' '.join(mots2[y:y+ngram]), re.I):
            match1[i:i+ngram] = [1] * ngram
            match2[y:y+ngram] = [1] * ngram

print('''
<html><head><meta http-equiv="Content-Type" content="text/html;charset=utf-8">
<style>
    .highlight{background-color:yellow ;}
     .container{position: absolute;top:0;bottom:0;left:0;right:0;}
     .destination{position: absolute; top:0; bottom: 0; right: 0; width: 50%}
     .origin{position: absolute;top:0; left:0; bottom: 0; width: 50%}
     p{padding-bottom: 10px;}
     .frame {height: 90%; overflow-y: auto;}
</style>
</head><body>
<div class="container">
<div class="origin">
<h2>Document d'origine</h2>
<div class="frame">
''')
printHighlight(mots1, match1)
print('''
</div>
</div>
<div class="destination">
<h2>Document similaire</h2>
<div class="frame">
''')
printHighlight(mots2, match2, sys.argv[2])
print('''
</div>
</div>
</div>
</body></html>
''')
