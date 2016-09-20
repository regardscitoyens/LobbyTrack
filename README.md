#Lobby Track

## Retrouver la trace des lobbys dans le travail des parlementaires

Ces deux scripts permettent de retrouver les copier/coller réalisés par les parlementaires à partir de documents (par exemple issus de lobbys).

Pour le faire fonctionner, il faut utiliser une version "texte brute" de documents produits par les lobbys.

Ce document texte sera confronté aux moteurs de recherche de NosDéputés.fr et/ou NosSénateurs.fr via le script *queryFromTxt.sh*.

Le script *highlightTrack.py* permet de représenter graphiquement les éléments communs dans les documents.

### queryFromTxt.sh

Pour rechercher les documents parlementaires de NosDéputés.fr qui reprennent des parties du fichier texte *document_lobby.txt* :

    bash queryFromTxt.sh document_lobby.txt nosdeputes.fr

Pour trouver les documents sénatoriaux :

    bash queryFromTxt.sh document_lobby.txt nossenateurs.fr

Ces scripts produisent des fichiers triés par pertinence pour chaque document intéressant dans le même répertoire que celui où se situait le fichier initial (plus pertinent en premier) :

Pour NosDéputés.fr (avec un n-gram de 5 mots) :

    document_lobby.txt.nosdeputes.fr.5mots.txt

Pour NosSénateurs :

    document_lobby.txt.nossenateurs.fr.5mots.txt

### highlightTrack.py

Pour comparer un document parlementaire (en texte brut) avec le document original :

    python3 highlightTrack.py document_lobby.txt document_parlementaire.txt > highlight.html

Pour changer le n-gram, ajouter son nombre en troisième paramètre comme sur l'exemple suivant :

    python3 highlightTrack.py document_lobby.txt document_parlementaire.txt 3 > highlight_3gram.html


Le fichier résultant *highlight.html* permet une comparaison graphique des deux documents.

Voici un exemple avec une liasse d'amendements soumise aux parlementaire par l'[ANIA](http://www.ania.net/alimentation-sante/etiquetage2005) et l'[un des amendements trouvés](http://nosdeputes.fr/14/amendement/2302/AS685) :

![Exemple de comparaison de documents](highlight.jpg)
