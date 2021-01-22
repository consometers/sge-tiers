## Homologation

Exemple d’accès à un service web sur la plateforme d’homologation en utilisant :

- l’identifiant `homologation@dupont.fr` et le mot de passe `enedis1234`,
- le certificat `fullchain.pem` préalablement transmis à Enedis,
- la clé privée correspondante `privkey.pem`.

Requête enregistrée dans le fichier `request.xml` :

```xml
<?xml version='1.0' encoding='utf-8'?>
<soap-env:Envelope xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/">
    <soap-env:Body>
        <ns0:rechercherPoint xmlns:ns0="http://www.enedis.fr/sge/b2b/services/rechercherpoint/v2.0">
            <criteres>
                <adresseInstallation>
                    <numeroEtNomVoie>404 RUE DES CIMBRES</numeroEtNomVoie>
                    <codePostal>83380</codePostal>
                    <codeInseeCommune>83107</codeInseeCommune>
                </adresseInstallation>
                <nomClientFinalOuDenominationSociale>Homologation</nomClientFinalOuDenominationSociale>
                <rechercheHorsPerimetre>true</rechercheHorsPerimetre>
            </criteres>
            <loginUtilisateur>homologation@dupont.fr</loginUtilisateur>
        </ns0:rechercherPoint>
    </soap-env:Body>
</soap-env:Envelope>
```

En utilisant `curl` :

```
curl --verbose --user homologation@dupont.fr:enedis1234 \
  --key privkey.pem \
  --cert fullchain.pem \
  -X POST -H "Content-Type: application/soap+xml" \
  --data-binary @request.xml \
  https://sge-homologation-b2b.enedis.fr/RecherchePoint/v2.0
```

En utilisant `wget` :

```
wget --ca-cert=ca.pem --certificate=fullchain.pem --private-key=privkey.pem --http-user=homologation@dupont.fr --http-password=enedis1234 --post-file=request.xml --header="Content-Type: application/soap+xml"  https://sge-homologation-b2b.enedis.fr/RecherchePoint/v2.0 -O response.xml
```