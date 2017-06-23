#!coding: utf-8

import sys
import re
import json

ngram = 4

def file2array(file):
    txt = re.sub(u"[\?\+‑\.!,;–()'’-]", " ", file.read().decode('UTF-8'))
    txt = txt.replace('|', ' ')
    txt = txt.replace(u'’', '\'')
    txt = re.sub('\n+', ' <br/> ', txt)
    txt = re.sub(u' *([«"»:;]) *', r' " ', txt)
    txt = re.sub('L(\d)', r'L \1', txt)
    return [mot for mot in re.split("\s+", txt) if mot]

def printHighlight(mots, withnbmots="", prefix="l"):
    html = ''
    nb = 0
    max = 0
    for i, mot in enumerate(mots):
        id_i = prefix+str(i)
        if word_to_groups[id_i]:
            html += '<span class="highlight" name="word" id="'+id_i+'" onmouseout="trigger([])" onmouseover="trigger('+str(word_to_groups[id_i])+')">'
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

def longest_common_subsequence(list1, list2, i1, i2):
    r"""
    Assuming that list1[i1] == list2[i2], this function extends the matching as
    far as possible to the left and to the right.

    Formally, the function returns the largest j,k such that :

        list1[i1-j:i1+k] == list2[i2-j:i2+k]

    """
    k=0
    for k in range(min(len(list1)-i1,len(list2)-i2)):
        if list1[i1+k] != list2[i2+k]:
            break
    j=0
    for j in range(min(i1,i2)+1):
        if list1[i1-j] != list2[i2-j]:
            break
    return (-j+1,k)

def words_to_pos(my_list):
    r"""
    Returns a dictionary associating to each element of set(my_list) the
    sequence of its positions in my_list
    """
    d = {}
    for i,x in enumerate(my_list):
        if x not in d:
            d[x] = []
        d[x].append(i)
    return d

with open(sys.argv[1], 'r') as f:
    mots1 = file2array(f)

with open(sys.argv[2], 'r') as f:
    mots2 = file2array(f)

if len(sys.argv) > 3 :
    ngram = int(sys.argv[3])

mots1_lower = [x.lower() for x in mots1] # convert to lower case
mots2_lower = [x.lower() for x in mots2] # convert to lower case

words_to_pos1 = words_to_pos(mots1_lower) # caches the positions of each word
words_to_pos2 = words_to_pos(mots2_lower) # caches the positions of each word

matchings = []
from itertools import product
for w,p1 in words_to_pos1.items(): # For any word w in mots1
    p2 = words_to_pos2.get(w,[])
    for i1,i2 in product(p1,p2): # Wor any i1,i2 such that mots1[i1]==most2[i2]
        j,k = longest_common_subsequence(mots1_lower,mots2_lower,i1,i2)
        if k-j >= ngram:
            matchings.append((i1+j,i2+j,k-j))

matchings = set(matchings) # contains the (i,j,k) such that mots1[i:i+k]==mots2[j:j+k]

# 'word_to_groups' associates each word to its groups
# 'group_to_words' associates each group to its words
word_to_groups = {'left'+str(i):[] for i,_ in enumerate(mots1)} # Associates each word to its groups
word_to_groups.update({'right'+str(i):[] for i,_ in enumerate(mots2)})

group_to_words = [] # Associates each group to its words
for group_id,(i,j,k) in enumerate(matchings):
    group_to_words.append([])
    for x in range(k):
        word_to_groups['left'+str(i+x)].append(group_id)
        word_to_groups['right'+str(j+x)].append(group_id)
        group_to_words[group_id].extend(['left'+str(i+x),'right'+str(j+x)])

sys.stderr.write("Matchings found:\n\n")
for i,j,k in matchings:
    sys.stderr.write(' '.join(mots1[i:i+k])+"\n")


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
<script>
group_to_words='''+json.dumps(group_to_words)+''';
function trigger(x) {
   allwords=document.getElementsByName("word");
   for(i=0;i<allwords.length;++i) {
     allwords[i].style.backgroundColor='';
   }
   for(i=0;i<x.length;++i){
       group=group_to_words[x[i]];
       for(j=0;j<group.length;++j) {
         document.getElementById(group[j]).style.backgroundColor='FFDD00';
       }
   }
};
</script>
</head><body>
<div class="container">
<div class="origin">
<h2>Document d'origine</h2>
<div class="frame">
''')
printHighlight(mots1, prefix="left")
print('''
</div>
</div>
<div class="destination">
<h2>Document similaire</h2>
<div class="frame">
''')
printHighlight(mots2, sys.argv[2],prefix="right")
print('''
</div>
</div>
</div>
</body></html>
''')
