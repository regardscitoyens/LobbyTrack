#!/bin/bash

DIRBIN="./"$(dirname $0)

CSVMOTS=$1
TXTMOTS=$(echo "$CSVMOTS" | sed 's/\.txt.nossenateurs.fr.5mots.txt/.txt/')
DIRMOTS=$(echo $TXTMOTS | sed 's/.txt//' | sed 's/ /_/g' | sed "s/'//ig")"/html"

mkdir -p "$DIRMOTS"

cat "$CSVMOTS" |  grep -v Texteloi | awk -F ';' '{print "echo DIRMOTS/"$3".txt ; #curl -s http://www.nossenateurs.fr"$4" | sed @s/<[^>]*>/\\n/g@ | sed @s/.amp;lt;/</g@ | sed @s/.amp;gt;/>/g@  | sed @s/<[^>]*>//g@ > @DIRMOTS/"$3".txt@" }' | sed 's/@/"/g' | sed "s@DIRMOTS@$DIRMOTS@g" > /tmp/sh.txt 

bash /tmp/sh.txt | head -n 1000 | while read file ; do 
	echo python $DIRBIN/highlightTrack.py '"'$TXTMOTS'"' $file
	python $DIRBIN/highlightTrack.py "$TXTMOTS" $file > $file.html  
done 2> "$TXTMOTS"".nbmots.csv"
cat "$TXTMOTS"".nbmots.csv" | sed 's/;[^0-9][^;]*html./;/' | sed 's/.txt//' | sort -t ';' -k 2,2 > "$TXTMOTS"".nbmots.sorted.csv"

sort -t ';' -k 3,3 "$CSVMOTS" > "$CSVMOTS"".sorted.csv"
join -t ';' -1 2 -2 3 "$TXTMOTS"".nbmots.sorted.csv" "$CSVMOTS"".sorted.csv" | sort -t ';' -k 2,2 -n > "$TXTMOTS"".proximite.csv"
