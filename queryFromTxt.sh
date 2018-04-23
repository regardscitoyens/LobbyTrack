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
MOTSTXT=$(cat "$TXT".mots | wc -l)
echo "$MOTSTXT mots identifiés dans le texte d'origine"
echo "- La liste est visible dans $TXT.mots"

# Pour toute suite de $NBMOTS mots, on recherche sur $SITE
mapfile -t words_array < $TXT.mots
for (( i = 0 ; i < $MOTSTXT-$NBMOTS ; i++ )); do
    words="$(echo ${words_array[@]:$i:$NBMOTS} | $SED_CMD "s/ /%20/g")"
    curl -s -L "http://$SITE/recherche/$words?format=csv"
done |
    tee "$TXT"."$SITE2".csv | # stockage
    grep '/csv$' | sort | uniq -c  | sort -rn | $SED_CMD 's|/csv|/xml|' |
    awk '{if ( $1 > 7 ) print $1" "$2}' > "$TXT"."$SITE"."$NBMOTS"mots.txt # Si au moins 7 occurrences, c'est un match

echo "Consulter $TXT.$SITE.${NBMOTS}mots.txt pour voir les résultats"
