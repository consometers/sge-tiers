# Utilisation du service SGE Tiers d’Enedis

Enedis fournit un accès aux données de consommation électrique si vous êtes un client ou un tiers autorisé par le client.

Cet accès necessite des démarches administratives assez lourdes, il est donc plutôt destiné à des entreprises ou des associations souhaitant accéder aux données de consommation de manière régulière ou sur un parc de compteurs important.

<table>
  <thead>
    <tr>
      <td colspan="2"></td>
      <td colspan="3">Accès aux données</td>
    </tr>
    <tr>
      <th>Phase</th>
      <th>Délais</th>
      <th>Mail</th>
      <th>Web</th>
      <th>API</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Inscription sur DataHub</td>
      <td></td>
      <td>❌</td>
      <td>❌</td>
      <td>❌</td>
    </tr>
    <tr>
      <td>Souscription au service Dataconsoelec</td>
      <td>2 semaines</td>
      <td>✔️</td>
      <td>❌</td>
      <td>❌</td>
    </tr>
    <tr>
      <td>Réunion de lancement SGE Tiers</td>
      <td>1 semaine</td>
      <td>✔️</td>
      <td>❌</td>
      <td>❌</td>
    </tr>
    <tr>
      <td>Contractualisation</td>
      <td>1 semaine</td>
      <td>✔️</td>
      <td>❌</td>
      <td>❌</td>
    </tr>
    <tr>
      <td>Référencement dans le système d’information</td>
      <td>1 mois</td>
      <td>✔️</td>
      <td>❌</td>
      <td>❌</td>
    </tr>
    <tr>
      <td>Réception de la clé PKI</td>
      <td>1 mois</td>
      <td>✔️</td>
      <td>✔️</td>
      <td>❌</td>
    </tr>
    <tr>
      <td>Réunion de lancement homologation</td>
      <td>1 semaine</td>
      <td>✔️</td>
      <td>✔️</td>
      <td>❌</td>
    </tr>
    <tr>
      <td>Échange de certificats SSL homologation</td>
      <td>1 semaine</td>
      <td>✔️</td>
      <td>✔️</td>
      <td>❌</td>
    </tr>
    <tr>
      <td>Homologation</td>
      <td></td>
      <td>✔️</td>
      <td>✔️</td>
      <td>❌</td>
    </tr>
    <tr>
      <td>Échange de certificats SSL prod</td>
      <td></td>
      <td>✔️</td>
      <td>✔️</td>
      <td>✔️</td>
    </tr>
  </tbody>
</table>

## Services permettant d’accéder aux données

### Dataconsoelec: demande par mail

Après avoir été référencé par Enedis il suffit d’envoyer par mail une liste de point de PRM associée à une période. Les données sont ensuite envoyées par retour de mail.

Avantages :

- Adapté à des demandes de données ponctuelles
- Pas besoin de SIRET (à vérifier)
- Accès rapide

Limitations :

- L’accès demande une intervention manuelle, pas forcément adapté à des demandes régulière

Références :

- [Accéder aux données de mesure](https://www.enedis.fr/acceder-aux-donnees-de-mesure) sur le site d’Enedis

*[PRM]: Point Référence Mesure, identifiant du compteur

TODO: Index de consomation et heures pleines / heures creuses accessible ?

### Data Connect: accès par une API aux données Linky

Avantages :

- Recueil du consentement par Enedis, intégré à l’API
- Permet un accès automatisé et régulier
- API REST moderne, documentation accessible

Limitations :

- Concerne uniquement les données de compteurs Linky raccordés avec une puissance inférieure à 36 kVA
- Certaines données ne sont pas encore exposées
  - index de consommation
  - répartition heures pleines / heures creuses
- Nécessite un numéro de SIRET et une contractualisation avec Enedis
- Nécessite des connaissances en programmation
- Un essai sur un environnement « bac à sable » doit être développé avant d’accéder à de vraies données

Références :

- [Data Connect sur le DataHub Enedis](https://datahub-enedis.fr/data-connect/)
- [Notre dépôt dédié au Data Connect](https://github.com/consometers/data-connect)

### Portail SGE Tiers: accès par un portail Web

Avantages :

- Données les plus complètes, seul moyen d’accéder :
  - aux mesures de compteurs raccordés avec une puissance supérieure à 36 kVA
  - aux index de consommation
  - à la recherche de PRM
- Accès Web, ne nécessite pas de connaissances en programmation
- Permet un accès automatisé et régulier par la souscription à des flux de données, envoyées par mail ou FTP

Limitations :

- Nécessite un numéro de SIRET et une contractualisation avec Enedis
- Démarches administratives assez longues (compter plusieurs mois)
- Documentation peu accessible pour les non-initiés à l’infrastructure d’Enedis, son système d’information et ses termes techniques

Références :

- Cette page !
- [SGE Tiers sur le DataHub Enedis](https://datahub-enedis.fr/sge-tiers/)

### Webservice: accès par une API

API SOAP permettant d’effectuer les mêmes actions que sur le portail Web de manière automatisée.