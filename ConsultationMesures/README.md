
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

PRM anonymisé 09111642617347

Requête :

```xml
<?xml version="1.0" ?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:tec="http://www.enedis.fr/sge/b2b/technique/v1.0" xmlns:ns0="http://www.enedis.fr/sge/b2b/services/consultermesures/v1.1" xmlns:ns1="http://schemas.xmlsoap.org/soap/envelope/">
    <SOAP-ENV:Header>
        <tec:entete>
            <version>1.1</version>
            <infoDemandeur>
                <loginDemandeur>sge-tiers@votre-entreprise.fr</loginDemandeur>
            </infoDemandeur>
        </tec:entete>
    </SOAP-ENV:Header>
    <ns1:Body>
        <ns0:consulterMesures>
            <pointId>09111642617347</pointId>
            <loginDemandeur>sge-tiers@votre-entreprise.fr</loginDemandeur>
            <contratId>2617347</contratId>
            <autorisationClient>true</autorisationClient>
        </ns0:consulterMesures>
    </ns1:Body>
</SOAP-ENV:Envelope>
```

Réponse :

```xml
<?xml version="1.0" ?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
  <soapenv:Header>
    <v1:acquittement xmlns:v1="http://www.enedis.fr/sge/b2b/technique/v1.0">
      <resultat code="SGT200">Succès</resultat>
      <infoFonctionnelles>
        <pointId>09111642617347</pointId>
      </infoFonctionnelles>
      <infoDemandeur>
        <loginDemandeur>sge-tiers@votre-entreprise.fr</loginDemandeur>
      </infoDemandeur>
    </v1:acquittement>
  </soapenv:Header>
  <soapenv:Body>
    <v1:consulterMesuresResponse xmlns:v1="http://www.enedis.fr/sge/b2b/services/consultermesures/v1.1">
      <seriesMesuresDateesGrilleTurpe>
        <serie>
          <grandeurPhysique code="EA">
            <libelle>Energie Active</libelle>
          </grandeurPhysique>
          <classeTemporelle code="BASE">
            <libelle>Base</libelle>
          </classeTemporelle>
          <calendrier code="DI000001">
            <libelle>Base</libelle>
          </calendrier>
          <unite>kWh</unite>
          <mesuresDatees>
            <mesure>
              <valeur>775</valeur>
              <dateDebut>2021-12-06</dateDebut>
              <dateFin>2022-01-06</dateFin>
              <nature code="REEL">
                <libelle>Réelle</libelle>
              </nature>
              <declencheur code="CYCLIQUE">
                <libelle>Publication cyclique</libelle>
              </declencheur>
              <statut code="INITIALE">
                <libelle>Initiale</libelle>
              </statut>
            </mesure>
            <mesure>
              <valeur>666</valeur>
              <dateDebut>2021-11-06</dateDebut>
              <dateFin>2021-12-06</dateFin>
              <nature code="REEL">
                <libelle>Réelle</libelle>
              </nature>
              <declencheur code="CYCLIQUE">
                <libelle>Publication cyclique</libelle>
              </declencheur>
              <statut code="INITIALE">
                <libelle>Initiale</libelle>
              </statut>
            </mesure>
            <mesure>
              <valeur>573</valeur>
              <dateDebut>2021-10-06</dateDebut>
              <dateFin>2021-11-06</dateFin>
              <nature code="REEL">
                <libelle>Réelle</libelle>
              </nature>
              <declencheur code="CYCLIQUE">
                <libelle>Publication cyclique</libelle>
              </declencheur>
              <statut code="INITIALE">
                <libelle>Initiale</libelle>
              </statut>
            </mesure>
            <mesure>
              <valeur>484</valeur>
              <dateDebut>2021-09-06</dateDebut>
              <dateFin>2021-10-06</dateFin>
              <nature code="REEL">
                <libelle>Réelle</libelle>
              </nature>
              <declencheur code="CYCLIQUE">
                <libelle>Publication cyclique</libelle>
              </declencheur>
              <statut code="INITIALE">
                <libelle>Initiale</libelle>
              </statut>
            </mesure>
            <mesure>
              <valeur>542</valeur>
              <dateDebut>2021-08-06</dateDebut>
              <dateFin>2021-09-06</dateFin>
              <nature code="REEL">
                <libelle>Réelle</libelle>
              </nature>
              <declencheur code="CYCLIQUE">
                <libelle>Publication cyclique</libelle>
              </declencheur>
              <statut code="INITIALE">
                <libelle>Initiale</libelle>
              </statut>
            </mesure>
            <mesure>
              <valeur>462</valeur>
              <dateDebut>2021-07-06</dateDebut>
              <dateFin>2021-08-06</dateFin>
              <nature code="REEL">
                <libelle>Réelle</libelle>
              </nature>
              <declencheur code="CYCLIQUE">
                <libelle>Publication cyclique</libelle>
              </declencheur>
              <statut code="INITIALE">
                <libelle>Initiale</libelle>
              </statut>
            </mesure>
            <mesure>
              <valeur>471</valeur>
              <dateDebut>2021-06-06</dateDebut>
              <dateFin>2021-07-06</dateFin>
              <nature code="REEL">
                <libelle>Réelle</libelle>
              </nature>
              <declencheur code="CYCLIQUE">
                <libelle>Publication cyclique</libelle>
              </declencheur>
              <statut code="INITIALE">
                <libelle>Initiale</libelle>
              </statut>
            </mesure>
            <mesure>
              <valeur>670</valeur>
              <dateDebut>2021-05-06</dateDebut>
              <dateFin>2021-06-06</dateFin>
              <nature code="REEL">
                <libelle>Réelle</libelle>
              </nature>
              <declencheur code="CYCLIQUE">
                <libelle>Publication cyclique</libelle>
              </declencheur>
              <statut code="INITIALE">
                <libelle>Initiale</libelle>
              </statut>
            </mesure>
            <mesure>
              <valeur>995</valeur>
              <dateDebut>2021-04-06</dateDebut>
              <dateFin>2021-05-06</dateFin>
              <nature code="REEL">
                <libelle>Réelle</libelle>
              </nature>
              <declencheur code="CYCLIQUE">
                <libelle>Publication cyclique</libelle>
              </declencheur>
              <statut code="INITIALE">
                <libelle>Initiale</libelle>
              </statut>
            </mesure>
            <mesure>
              <valeur>1126</valeur>
              <dateDebut>2021-03-06</dateDebut>
              <dateFin>2021-04-06</dateFin>
              <nature code="REEL">
                <libelle>Réelle</libelle>
              </nature>
              <declencheur code="CYCLIQUE">
                <libelle>Publication cyclique</libelle>
              </declencheur>
              <statut code="INITIALE">
                <libelle>Initiale</libelle>
              </statut>
            </mesure>
            <mesure>
              <valeur>1114</valeur>
              <dateDebut>2021-02-06</dateDebut>
              <dateFin>2021-03-06</dateFin>
              <nature code="REEL">
                <libelle>Réelle</libelle>
              </nature>
              <declencheur code="CYCLIQUE">
                <libelle>Publication cyclique</libelle>
              </declencheur>
              <statut code="INITIALE">
                <libelle>Initiale</libelle>
              </statut>
            </mesure>
            <mesure>
              <valeur>926</valeur>
              <dateDebut>2021-01-15</dateDebut>
              <dateFin>2021-02-06</dateFin>
              <nature code="REGU">
                <libelle>Régularisée</libelle>
              </nature>
              <declencheur code="CYCLIQUE">
                <libelle>Publication cyclique</libelle>
              </declencheur>
              <statut code="INITIALE">
                <libelle>Initiale</libelle>
              </statut>
            </mesure>
            <mesure>
              <valeur>30</valeur>
              <dateDebut>2021-01-11</dateDebut>
              <dateFin>2021-01-15</dateFin>
              <nature code="ESTI">
                <libelle>Estimée</libelle>
              </nature>
              <declencheur code="CYCLIQUE">
                <libelle>Publication cyclique</libelle>
              </declencheur>
              <statut code="INITIALE">
                <libelle>Initiale</libelle>
              </statut>
            </mesure>
          </mesuresDatees>
        </serie>
      </seriesMesuresDateesGrilleTurpe>
      <seriesMesuresDateesGrilleFrn>
        <serie>
          <grandeurPhysique code="EA">
            <libelle>Energie Active</libelle>
          </grandeurPhysique>
          <classeTemporelle code="BASE">
            <libelle>BASE</libelle>
          </classeTemporelle>
          <calendrier code="HoroF1">
            <libelle>HoroF1</libelle>
          </calendrier>
          <unite>kWh</unite>
          <mesuresDatees>
            <mesure>
              <valeur>1986</valeur>
              <dateDebut>2020-11-06</dateDebut>
              <dateFin>2021-01-07</dateFin>
              <nature code="REEL">
                <libelle>Réelle</libelle>
              </nature>
              <declencheur code="EVENEMENT">
                <libelle>Publication événementielle</libelle>
              </declencheur>
              <statut code="INITIALE">
                <libelle>Initiale</libelle>
              </statut>
            </mesure>
            <mesure>
              <valeur>310</valeur>
              <dateDebut>2020-10-20</dateDebut>
              <dateFin>2020-11-06</dateFin>
              <nature code="REEL">
                <libelle>Réelle</libelle>
              </nature>
              <declencheur code="CYCLIQUE">
                <libelle>Publication cyclique</libelle>
              </declencheur>
              <statut code="INITIALE">
                <libelle>Initiale</libelle>
              </statut>
            </mesure>
          </mesuresDatees>
        </serie>
        <serie>
          <grandeurPhysique code="EA">
            <libelle>Energie Active</libelle>
          </grandeurPhysique>
          <classeTemporelle code="BASE">
            <libelle>BASE</libelle>
          </classeTemporelle>
          <calendrier code="FC000165">
            <libelle>FC000165</libelle>
          </calendrier>
          <unite>kWh</unite>
          <mesuresDatees>
            <mesure>
              <valeur>775</valeur>
              <dateDebut>2021-12-06</dateDebut>
              <dateFin>2022-01-06</dateFin>
              <nature code="REEL">
                <libelle>Réelle</libelle>
              </nature>
              <declencheur code="CYCLIQUE">
                <libelle>Publication cyclique</libelle>
              </declencheur>
              <statut code="INITIALE">
                <libelle>Initiale</libelle>
              </statut>
            </mesure>
            <mesure>
              <valeur>666</valeur>
              <dateDebut>2021-11-06</dateDebut>
              <dateFin>2021-12-06</dateFin>
              <nature code="REEL">
                <libelle>Réelle</libelle>
              </nature>
              <declencheur code="CYCLIQUE">
                <libelle>Publication cyclique</libelle>
              </declencheur>
              <statut code="INITIALE">
                <libelle>Initiale</libelle>
              </statut>
            </mesure>
            <mesure>
              <valeur>573</valeur>
              <dateDebut>2021-10-06</dateDebut>
              <dateFin>2021-11-06</dateFin>
              <nature code="REEL">
                <libelle>Réelle</libelle>
              </nature>
              <declencheur code="CYCLIQUE">
                <libelle>Publication cyclique</libelle>
              </declencheur>
              <statut code="INITIALE">
                <libelle>Initiale</libelle>
              </statut>
            </mesure>
            <mesure>
              <valeur>484</valeur>
              <dateDebut>2021-09-06</dateDebut>
              <dateFin>2021-10-06</dateFin>
              <nature code="REEL">
                <libelle>Réelle</libelle>
              </nature>
              <declencheur code="CYCLIQUE">
                <libelle>Publication cyclique</libelle>
              </declencheur>
              <statut code="INITIALE">
                <libelle>Initiale</libelle>
              </statut>
            </mesure>
            <mesure>
              <valeur>542</valeur>
              <dateDebut>2021-08-06</dateDebut>
              <dateFin>2021-09-06</dateFin>
              <nature code="REEL">
                <libelle>Réelle</libelle>
              </nature>
              <declencheur code="CYCLIQUE">
                <libelle>Publication cyclique</libelle>
              </declencheur>
              <statut code="INITIALE">
                <libelle>Initiale</libelle>
              </statut>
            </mesure>
            <mesure>
              <valeur>462</valeur>
              <dateDebut>2021-07-06</dateDebut>
              <dateFin>2021-08-06</dateFin>
              <nature code="REEL">
                <libelle>Réelle</libelle>
              </nature>
              <declencheur code="CYCLIQUE">
                <libelle>Publication cyclique</libelle>
              </declencheur>
              <statut code="INITIALE">
                <libelle>Initiale</libelle>
              </statut>
            </mesure>
            <mesure>
              <valeur>471</valeur>
              <dateDebut>2021-06-06</dateDebut>
              <dateFin>2021-07-06</dateFin>
              <nature code="REEL">
                <libelle>Réelle</libelle>
              </nature>
              <declencheur code="CYCLIQUE">
                <libelle>Publication cyclique</libelle>
              </declencheur>
              <statut code="INITIALE">
                <libelle>Initiale</libelle>
              </statut>
            </mesure>
            <mesure>
              <valeur>670</valeur>
              <dateDebut>2021-05-06</dateDebut>
              <dateFin>2021-06-06</dateFin>
              <nature code="REEL">
                <libelle>Réelle</libelle>
              </nature>
              <declencheur code="CYCLIQUE">
                <libelle>Publication cyclique</libelle>
              </declencheur>
              <statut code="INITIALE">
                <libelle>Initiale</libelle>
              </statut>
            </mesure>
            <mesure>
              <valeur>995</valeur>
              <dateDebut>2021-04-06</dateDebut>
              <dateFin>2021-05-06</dateFin>
              <nature code="REEL">
                <libelle>Réelle</libelle>
              </nature>
              <declencheur code="CYCLIQUE">
                <libelle>Publication cyclique</libelle>
              </declencheur>
              <statut code="INITIALE">
                <libelle>Initiale</libelle>
              </statut>
            </mesure>
            <mesure>
              <valeur>1126</valeur>
              <dateDebut>2021-03-06</dateDebut>
              <dateFin>2021-04-06</dateFin>
              <nature code="REEL">
                <libelle>Réelle</libelle>
              </nature>
              <declencheur code="CYCLIQUE">
                <libelle>Publication cyclique</libelle>
              </declencheur>
              <statut code="INITIALE">
                <libelle>Initiale</libelle>
              </statut>
            </mesure>
            <mesure>
              <valeur>1114</valeur>
              <dateDebut>2021-02-06</dateDebut>
              <dateFin>2021-03-06</dateFin>
              <nature code="REEL">
                <libelle>Réelle</libelle>
              </nature>
              <declencheur code="CYCLIQUE">
                <libelle>Publication cyclique</libelle>
              </declencheur>
              <statut code="INITIALE">
                <libelle>Initiale</libelle>
              </statut>
            </mesure>
            <mesure>
              <valeur>926</valeur>
              <dateDebut>2021-01-15</dateDebut>
              <dateFin>2021-02-06</dateFin>
              <nature code="REGU">
                <libelle>Régularisée</libelle>
              </nature>
              <declencheur code="CYCLIQUE">
                <libelle>Publication cyclique</libelle>
              </declencheur>
              <statut code="INITIALE">
                <libelle>Initiale</libelle>
              </statut>
            </mesure>
            <mesure>
              <valeur>30</valeur>
              <dateDebut>2021-01-11</dateDebut>
              <dateFin>2021-01-15</dateFin>
              <nature code="ESTI">
                <libelle>Estimée</libelle>
              </nature>
              <declencheur code="CYCLIQUE">
                <libelle>Publication cyclique</libelle>
              </declencheur>
              <statut code="INITIALE">
                <libelle>Initiale</libelle>
              </statut>
            </mesure>
            <mesure>
              <valeur>195</valeur>
              <dateDebut>2021-01-07</dateDebut>
              <dateFin>2021-01-11</dateFin>
              <nature code="REEL">
                <libelle>Réelle</libelle>
              </nature>
              <declencheur code="EVENEMENT">
                <libelle>Publication événementielle</libelle>
              </declencheur>
              <statut code="INITIALE">
                <libelle>Initiale</libelle>
              </statut>
            </mesure>
          </mesuresDatees>
        </serie>
      </seriesMesuresDateesGrilleFrn>
    </v1:consulterMesuresResponse>
  </soapenv:Body>
</soapenv:Envelope>
```

## Exemple pour les autres points

## Références

Guide d'implémentation du Service B2B ConsultationMesures, Version 1.1 du service, Enedis.SGE.GUI.0455 v1.0.0. 