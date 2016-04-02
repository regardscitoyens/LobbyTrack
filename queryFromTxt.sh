#!/bin/bash

TXT=$1
SITE=$2
NBMOTS=5
if ! test "$SITE"; then
SITE=nosdeputes.fr
fi

if ! test "$TXT" ; then
	echo "Usage: "
	echo "\t$0 document.txt nosdeputes.fr"
        echo "\t$0 document.txt nossenateurs.fr"
	exit 1;
fi

cat "$TXT" | sed 's/ /\n/g' > "$TXT".mots
MOTSTXT=$(wc -l "$TXT".mots | sed 's/ .*//')

for (( i = $NBMOTS ; i < $MOTSTXT ; i++ )) ; do echo $(cat "$TXT".mots | sed 's/ /\n/g' | head -n $i | tail -n $NBMOTS | grep -v '*' ) ; done | sed 's/ /%20/g' | sed 's|^|curl -s -L http://'$SITE'/recherche/"|' | sed 's|$|"?format=csv|' | bash > "$TXT"."$SITE".csv

cat "$TXT"."$SITE".csv | grep -v '^type document' | grep 'csv' | sort | uniq -c  | sort -rn | sed 's|/csv|/xml|' | awk '{if ( $1 > 7 ) print $1" "$2}' > "$TXT"."$SITE"."$NBMOTS"mots.txt

