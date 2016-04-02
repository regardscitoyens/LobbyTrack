#!coding: utf-8

import sys
import re

def file2array(file):
    mots = []
    for mot in re.split("\s+", re.sub('L(\d)', r'L \1', re.sub('([«"»])', r' \1 ', re.sub('\n+', ' <br/> ', re.sub(u'’', "'", re.sub("[‑\.!,;–()'-]", " ", file.read())))))):
        if mot:
            mots.append(mot)
    return mots

def printHighlight(mots, match):
    html = ''
    for i in range (0, len(mots)):
        if match[i]:
            html += '<span class="highlight">';
        else:
            html += '<span>';
        html += mots[i]
        html += ' </span>';
    html = '<p>'+re.sub('<br/>', '</p><p>', html)+'</p>'
    print(html)

f = open(sys.argv[1], 'r')
mots1 = file2array(f)
f.close()

f = open(sys.argv[2], 'r')
mots2 = file2array(f)
f.close()

match1 = [0] * len(mots1)
match2 = [0] * len(mots2)

for i in range(0, len(mots1) - 4):
    for y in range(0, len(mots2) - 4):
        if re.match(' '.join(mots1[i:i+4]), ' '.join(mots2[y:y+4]), re.I):
            match1[i:i+4] = [1] * 4
            match2[y:y+4] = [1] * 4

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
printHighlight(mots2, match2)
print('''
</div>
</div>
</div>
</body></html>
''')
