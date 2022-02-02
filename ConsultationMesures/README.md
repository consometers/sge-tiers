
# ConsultationMesures V1.1

Historique des consommations restituées sur la grille Distributeur et/ou la grille Fournisseur.

- profondeur maximale de douze mois limitée par la date de dernière mise en service
- disponible sur tous les segments (C1-C5)

| Segment | Grille distributeur | Grille fournisseur |
|---|---|---|
| C1[^1] | Oui | Non |
| C2-C4 | Oui | Si définie |
| C5 Nouvelle chaine | Oui | Oui |
| C5 Ancienne chaine | Non | Oui |

[^1]: Non disponible pour les points C1 raccordés au domaine de tension HTA

## Exemple point du segment C5 migré dans la nouvelle chaîne

- PRM anonymisé [09111642617347](/prms.md#09111642617347)
- [Requête (SOAP)](./C5/request.xml)
- [Réponse (SOAP)](./C5/response.xml)

## Exemple pour les autres points

- PRM anonymisé [30001642617347](/prms.md#30001642617347)
- [Requête (SOAP)](./C4/request.xml)
- [Réponse (SOAP)](./C4/response.xml)

## Références

Guide d'implémentation du Service B2B ConsultationMesures, Version 1.1 du service, Enedis.SGE.GUI.0455 v1.0.0. 