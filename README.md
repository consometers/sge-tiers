# Utilisation du service SGE Tiers d’Enedis

## Comparaison avec les autres services

L’accès à SGE Tiers est assez complexe (compter plusieurs mois), il est plutôt destiné à des entreprises ou des associations souhaitant accéder aux données de consommation de manière régulière ou sur un parc de compteurs important. Voici pour commencer un comparatif avec les autres services disponibles pour accéder à des données de consommation.

### Dataconsoelec: demande par mail

Après avoir été référencé par Enedis il suffit d’envoyer par mail une liste de point de <acronym title="Point Référence Mesure, identifiant du compteur">PRM</acronym> associée à une période. Les données sont ensuite envoyées par retour de mail.

**Avantages**

- Adapté à des demandes de données ponctuelles
- Ne nécessite pas de SIRET
- Accès rapide

**Limitations**

- L’accès demande une intervention manuelle, pas forcément adapté à des demandes régulières

**Références**

- [Accéder aux données de mesure](https://www.enedis.fr/acceder-aux-donnees-de-mesure) sur le site d’Enedis

### Data Connect: accès par une API aux données Linky

**Avantages**

- Recueil du consentement par Enedis, intégré à l’API
- Permet un accès automatisé et régulier
- API REST moderne, documentation accessible

**Limitations**

- Concerne uniquement les données de compteurs Linky raccordés avec une puissance inférieure à 36 kVA
- Certaines données ne sont pas encore exposées
  - index de consommation
  - répartition heures pleines / heures creuses
- Nécessite un numéro de SIRET et une contractualisation avec Enedis
- Nécessite des connaissances en programmation
- Un essai sur un environnement « bac à sable » doit être développé avant d’accéder à de vraies données

**Références**

- [Data Connect sur le DataHub Enedis](https://datahub-enedis.fr/data-connect/)
- [Notre dépôt dédié au Data Connect](https://github.com/consometers/data-connect)

### Portail SGE Tiers: accès par un portail Web

**Avantages**

- Données les plus complètes, permet notamment l’accès aux mesures de compteurs raccordés avec une puissance supérieure à 36 kVA, à la recherche de PRM et aux index de consommation en heures creuses / heures pleines
- Accès Web, ne nécessite pas de connaissances en programmation
- Permet un accès automatisé et régulier par la souscription à des flux de données, envoyées par mail ou FTP

**Limitations**

- Nécessite un numéro de SIRET et une contractualisation avec Enedis
- Démarches administratives très longues
- Documentation peu accessible pour les non-initiés à l’infrastructure d’Enedis, son système d’information et ses termes techniques

**Références**

- Cette page !
- [SGE Tiers sur le DataHub Enedis](https://datahub-enedis.fr/sge-tiers/)

### Webservice: accès par une API

API SOAP permettant d’effectuer les mêmes actions que sur le portail Web de manière automatisée.

## Souscription à SGE Tiers

Voici notre expérience à la mi-2020.

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
      <td><a href="#inscription-sur-datahub">Inscription sur DataHub</a></td>
      <td></td>
      <td>❌</td>
      <td>❌</td>
      <td>❌</td>
    </tr>
    <tr>
      <td><a href="#referencement-par-dataconsoelec">Référencement par Dataconsoelec</a></td>
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
      <td>2 semaines</td>
      <td>✔️</td>
      <td>✔️</td>
      <td>❌</td>
    </tr>
    <tr>
      <td>Échange de certificats SSL prod</td>
      <td>1 semaine</td>
      <td>✔️</td>
      <td>✔️</td>
      <td>✔️</td>
    </tr>
  </tbody>
</table>

⚠️ Le renouvellement d’un certificat SSL peut également prendre plusieurs semaines.

### Inscription sur DataHub

La demande d’accès à SGE Tiers s’effectue sur le [DataHub Enedis](https://datahub-enedis.fr/), accessible après la création d’un compte.

### Référencement par Dataconsoelec

Un numéro de référencement Enedis est également nécessaire pour souscrire à SGE Tiers. Il semble que la manière de l’obtenir soit de souscrire au service Dataconsoelec en demandant l’accès aux données d’un tiers.

Se référer à cette [procédure][dataconsoelec-procedure].

En résumé, envoyer une demande de référencement à <dataconsoelec@enedis.fr> :
- Le [formulaire de référencement][dataconsoelec-referencement]
- La copie des justificatifs
- Le PRM d’un site de consommation concernant un tiers, ainsi que les données à obtenir (par exemple l’historique de courbe de charge)
- Le [formulaire de consentement du tiers concerné][dataconsoelec-autorisation]

Le numéro de référencement Enedis vous sera ensuite attribué.

[dataconsoelec-procedure]: https://www.enedis.fr/sites/default/files/Enedis-OPE-CF_08E.pdf "Procédure de communication à un client ou à un tiers autorisé de données relatives à un site de consommation raccordé au sréseau public de distribution géré par Enedi[s"

[dataconsoelec-referencement]: https://www.enedis.fr/sites/default/files/Enedis_Demande_de_referencement_tiers_autorise.pdf "Demande de référencement d’un tiers pour la communication des données de site(s) de consommation raccordé(s) au réseau public de distribution"

[dataconsoelec-autorisation]: https://www.enedis.fr/sites/default/files/Enedis_Modele_Autorisation_individuelle_client.pdf "Modèle d’autorisation de communication à un tiers des données d’un ou plusieurs sites de consommations raccordés au réseau public de distribution"