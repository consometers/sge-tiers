# CommandeCollectePublicationMesures V3.0

Pour les points C5 Linky ouverts aux nouveaux services (avec un niveau d’ouverture aux services égal à 2) :

- activer la collecte de la courbe de charge
- souscrire à la transmission récurrente de la courbe de charge
- souscrire à la transmission récurrente des index quotidiens et des puissances max quotidiennes

Pour les points P4 ouverts aux nouveaux services (avec un niveau d’ouverture aux services égal à 2) :

- activer la collecte de la courbe de charge

Pour les points C1-C4 ou P1-P3 :

- activer la collecte de courbes enrichies (de charge et de tension)
- souscrire à la transmission récurrente de courbes enrichies
- souscrire à la transmission quotidienne des index et des autres données du compteur, inclut également la transmission des données sur glissement à chaque changement de période contractuelle

Pour tous les points :

- renouveller la souscription d’un service déjà actif

## Souscription courbe de charge

### C5 ouverts aux nouveaux services (courbe de charge)

- PRM anonymisé [09111642617347](/prms.md#09111642617347)
- [Requête (SOAP)](./C5-CDC/request.xml)
- [Réponse (SOAP)](./C5-CDC/response.xml)
- [Flux R50 (XML)](./C5-CDC/R50.xml) reçu quotidiennement

### C4 (courbe de charge et tension)

- PRM anonymisé [30001642617347](/prms.md#30001642617347)
- [Requête (SOAP)](./C4-CDC/request.xml)
- [Réponse (SOAP)](./C4-CDC/response.xml)
- [Flux R4Q (XML)](./C4-CDC/R4Q.xml) reçu quotidiennement

## Souscription index

### C5 ouverts aux nouveaux services (index et puissance max)

- PRM anonymisé [09111642617347](/prms.md#09111642617347)
- [Requête (SOAP)](./C5-IDX/request.xml)
- [Réponse (SOAP)](./C5-IDX/response.xml)
- [Flux R151 (XML)](./C5-IDX/R151.xml) reçu quotidiennement

### C4 (index et autres données)

- PRM anonymisé [30001642617347](/prms.md#30001642617347)
- [Requête (SOAP)](./C4-IDX/request.xml)
- [Réponse (SOAP)](./C4-IDX/response.xml)
- [Flux R171 (XML)](./C4-IDX/R171.xml) reçu quotidiennement
