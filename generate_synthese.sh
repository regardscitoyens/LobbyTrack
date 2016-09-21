#!/bin/bash

echo '<html><meta charset="utf-8"/><body>' > synthese.html
rgrep ';' txt/*/*.proximite.csv  | sed 's/:/;/' | sort -r  -n -t ';' -k 3,3 | sed 's|.txt.proximite.csv;|/html/|'  | awk -F ';' '{if ( $2 > 10 ) print "<p>"$1" : <a href=@"$1".txt.html@>"$4" "$2" mots communs</a> <a href=@http://nossenateurs.fr"$5"@>Source "$4"</a></p>"}'  | sed 's/@/"/g' | sed 's|txt/||' | sed 's|/[^<]*<| : <|' >> synthese.html
echo "</body></html>" >> synthese.html

