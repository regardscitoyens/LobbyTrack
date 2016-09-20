#!/bin/bash

# If needed use a different sed command version
SED_CMD="sed"

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

# Isoler chaque mot sur une ligne différente
cat "$TXT" | $SED_CMD 's/ /\n/g' > "$TXT".mots
MOTSTXT=$(wc -l "$TXT".mots | $SED_CMD 's/ .*//')
echo "$MOTSTXT mots identifiés dans le texte d'origine"
echo "- La liste est visible dans $TXT.mots"

for (( i = $NBMOTS ; i < $MOTSTXT ; i++ )) ; do echo $(cat "$TXT".mots | $SED_CMD  's/ /\n/g' | head -n $i | tail -n $NBMOTS | grep -v '*' ) ; done | $SED_CMD  's/ /%20/g' | $SED_CMD  's|^|curl -s -L http://'$SITE'/recherche/"|' | $SED_CMD  's|$|"?format=csv|' | bash > "$TXT"."$SITE".csv

cat "$TXT"."$SITE".csv | grep -v '^type document' | grep 'csv' | sort | uniq -c  | sort -rn | $SED_CMD  's|/csv|/xml|' | awk '{if ( $1 > 7 ) print $1" "$2}' > "$TXT"."$SITE"."$NBMOTS"mots.txt

echo "Consulter $TXT.$SITE.${NBMOTS}mots.txt pour voir les résultats"
