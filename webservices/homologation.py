#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# modules : python3-zeep

import os
import argparse
import unittest
import logging.config
import json

import sge

parser = argparse.ArgumentParser()
parser.add_argument("conf", help="Configuration file (typically private/*.conf.json)")
parser.add_argument('tests', type=str, nargs='*',
                    help='List of tests to run, like TestConsultationMesures.test_ahc_r1')
args = parser.parse_args()

logging.basicConfig()
debug = []

#debug.append("urllib3")
#debug.append("zeep.wsdl")
#debug.append("zeep.transports")

for logger in debug:
    logger = logging.getLogger(logger)
    logger.setLevel(logging.DEBUG)
    logger.propagate = True

with open(args.conf, 'r') as json_file:
    conf = json.load(json_file)

# Revolves path relative to configuration file
def conf_abspath(key):
    cwd = os.getcwd()
    try:
        os.chdir(os.path.dirname(args.conf))
        path = conf[key]
        path = os.path.expanduser(path)
        path = os.path.abspath(path)
        return path
    finally:
        os.chdir(cwd)

# Made server certificate with
# cat enedis-cert.pem SSL\ OV_Quovadis/intermdiaire/QuoVadis_OV_SSL_ICA_G3.pem  SSL\ OV_Quovadis/racine/QuoVadis_Root_CA_2_G3.pem > enedis-fullchain.pem

session = sge.Session(wsdl_root=conf_abspath('WSDL_FILES_ROOT'),
                      login=conf['LOGIN'],
                      contract_id=conf['CONTRACT_ID'],
                      client_certificates=conf_abspath('CERT_FULLCHAIN'),
                      client_privkey=conf_abspath('CERT_PRIVKEY'),
                      server_certificates='./server-fullchain.pem',
                      homologation=True)

class TestRechercherPoint(unittest.TestCase):

    def setUp(self):
        self.service = sge.RechercherPoint(session)

    def test_rp_r1(self):
        """RP-R1 Recherche à partir de critères autres que les données du client

        Pré-requis

        L’acteur tiers dispose d’informations n’étant pas relatives au client pour le point à rechercher.

        Descriptif

        L’acteur tiers précise dans sa demande:
        - L’acteur tiers précise dans sa demande:
        - Le couple {code postal, code INSEE},
        - Le domaine de tension,
        - La catégorie du client final

        Résultat attendu

        La demande est recevable.
        Une liste de moins de 200 points est retournée en résultat.

        JDD

        Code postal : 75001
        Code INSEE : 75101
        Domaine de tension : HTA
        Catégorie du client :PRO
        """

        criteres = {
            'adresseInstallation': {
                'codePostal': 75001,
                'codeInseeCommune': 75101,
                },
            'domaineTensionAlimentationCode': 'HTA',
            'categorieClientFinalCode': 'PRO'
        }

        res = self.service.rechercher(criteres)
        self.assertEqual('SGT200', res['code'])
        self.assertTrue(len(res['data']) < 200)

    def test_rp_r2(self):
        """RP-R2 Recherche du N° de PRM à partir de l’adresse et du nom exact du client pour un fournisseur non titulaire du point

        Pré-requis

        L’acteur tiers dispose d’informations n’étant pas relatives au client pour le point à rechercher.

        Descriptif

        L’acteur tiers précise dans sa demande:
        - Le code postal (13100)
        - Le code INSEE de la commune (13001)
        - L’adresse de l’installation (16 RUE DES MENUDIERES)
        - Le nom du client (« XXX »)
        - Qu’il s’agit d’une demande de recherche d’un point en service hors du périmètre

        Résultat attendu

        La demande est recevable.
        Un unique numéro de PRM est trouvé.
        """

        criteres = {
            'adresseInstallation': {
                'codePostal': 13100,
                'codeInseeCommune': 13001,
                'numeroEtNomVoie': '16 RUE DES MENUDIERES',
                },
            'nomClientFinalOuDenominationSociale': 'XXX',
            'rechercheHorsPerimetre': True
        }

        res = self.service.rechercher(criteres)
        self.assertEqual('SGT200', res['code'])
        self.assertEqual(1, len(res['data']))

    def test_rp_r3(self):
        """RP-R3 Recherche d’un point avec adresse exacte et nom approchant

        Pré-requis

        Recherche d’un point avec adresse exacte et nom approchant (chaîne de plus de trois caractères incluse dans le nom/dénomination sociale)

        Descriptif

        L’acteur tiers précise dans sa demande:
        - Le code postal (13100)
        - Le code INSEE de la commune (13001)
        - L’adresse de l’installation (16 RUE DES MENUDIERES)
        - Le nom ou dénomination sociale approchant du client (« XXX »)
        - Qu’il s’agit d’une demande de recherche d’un point en service hors du périmètre

        Résultat attendu

        La demande est recevable.
        Un unique numéro de PRM est trouvé.
        """

        criteres = {
            'adresseInstallation': {
                'codePostal': 13100,
                'codeInseeCommune': 13001,
                'numeroEtNomVoie': '16 RUE DES MENUDIERES',
                },
            'nomClientFinalOuDenominationSociale': 'XXX',
            'rechercheHorsPerimetre': True
        }

        res = self.service.rechercher(criteres)
        self.assertEqual('SGT200', res['code'])
        self.assertEqual(1, len(res['data']))

    def test_rp_nr1(self):
        """RP-NR1 Recherche avec des critères retournant plus de 200 points

        Pré-requis

        Recherche avec des critères retournant plus de 200 points.

        Descriptif

        L’acteur tiers précise dans sa demande:
        - Le couple {code postal, code INSEE},
        - La catégorie du client

        Résultat attendu

        Code retour : SGT4F8 – La recherche de points renvoie trop de résultats. Veuillez affiner les
        critères de recherche.
        """

        criteres = {
            'adresseInstallation': {
                'codePostal': 75001,
                'codeInseeCommune': 75101,
                },
            'domaineTensionAlimentationCode': 'BTINF',
            'categorieClientFinalCode': 'PRO'
        }

        res = self.service.rechercher(criteres)
        self.assertEqual('La recherche de points renvoie trop de résultats. Veuillez affiner les critères de recherche.', res['message'])
        self.assertEqual('SGT4F8', res['code'])

    def test_rp_nr2(self):
        """RP-NR2 Recherche avec des critères insuffisants

        Pré-requis

        Les critères choisis par l’acteur tiers ne sont pas suffisants.

        Descriptif

        L’acteur tiers précise dans sa demande:
        - Le code INSEE seul
        - L’adresse d’installation : numéro et nom de voie

        Résultat attendu

        Code retour : SGT4F7 – Les critères renseignés ne sont pas suffisants.
        """

        criteres = {
            'adresseInstallation': {
                'codeInseeCommune': 75101,
                'numeroEtNomVoie': '16 RUE DES MENUDIERES',
            }
        }

        res = self.service.rechercher(criteres)
        self.assertEqual('Les critères renseignés ne sont pas suffisants.', res['message'])
        self.assertEqual('SGT4F7', res['code'])

    def test_not_found(self):
        """Recherche sans résultat

        Retourne une liste vide
        """

        criteres = {
            'adresseInstallation': {
                'codePostal': 13100,
                'codeInseeCommune': 13001,
                'numeroEtNomVoie': '16 RUE DES MENUDIERES',
                },
            'nomClientFinalOuDenominationSociale': 'Jean Doe',
            'rechercheHorsPerimetre': True
        }

        res = self.service.rechercher(criteres)
        self.assertEqual('SGT200', res['code'])
        self.assertEqual(0, len(res['data']))

class TestConsultationDonneesTechniques(unittest.TestCase):

    def setUp(self):
        self.service = sge.ConsultationDonneesTechniquesContractuelles(session)

    def test_adp_r1(self):
        """ADP-R1 Accès aux données d’un point pour un acteur tiers avec une autorisation client

        Pré-requis

        Le PRM est en service.

        Descriptif

        Dans sa demande, l’acteur tiers précise notamment :
        - l’identifiant du point,
        - le login de l’utilisateur
        - qu’il dispose de l’autorisation client

        Résultat attendu

        Code retour : SGT200 – Succès. La demande est recevable. Les informations du point
        retournées sont conformes aux règles de filtrage ICS.
        """
        res = self.service.consulter("98800007059999")
        self.assertEqual('SGT200', res['code'])
        self.assertEqual("98800007059999", res['data']['id'])
        self.assertIsNotNone(res['data']['situationContractuelle'])

    def test_adp_r2(self):
        """ADP-R2 Accès aux données d’un point en service pour un acteur tiers sans autorisation client

        Pré-requis

        Le PRM est en service.

        Descriptif

        Dans sa demande, l’acteur tiers précise notamment :
        - l’identifiant du point,
        - le login de l’utilisateur
        - qu’il ne dispose pas de l’autorisation client.

        Résultat attendu

        Code retour : SGT200 – Succès. La demande est recevable. Les informations du point
        retournées sont conformes aux règles de filtrage ICS.
        """
        res = self.service.consulter("98800007059999", autorisation_client=False)
        self.assertEqual('SGT200', res['code'])
        self.assertEqual("98800007059999", res['data']['id'])
        self.assertIsNone(res['data']['situationContractuelle'])

    def test_adp_nr1(self):
        """ADP-NR1 Accès aux données d’un point inexistant

        Pré-requis

        PRM inexistant dans SGE.

        Descriptif

        Dans sa demande, l’acteur tiers précise :
        - l’identifiant du point,
        - le login de l’utilisateur
        - qu’il dispose ou non de l’autorisation client.

        Résultat attendu

        Code retour : SGT401 – Demande non recevable : point inexistant.
        """
        res = self.service.consulter("99999999999999", autorisation_client=False)
        self.assertEqual('Demande non recevable : point inexistant', res['message'])
        self.assertEqual('SGT401', res['code'])

class TestConsultationMesures(unittest.TestCase):

    def setUp(self):
        self.service = sge.ConsultationMesures(session)

    def test_ahc_r1(self):
        """AHC-R1 Accès à l’historique de consommations pour un acteur tiers avec une autorisation client

        Pré-requis

        Le PRM est en service.

        Descriptif

        Dans sa demande, l’acteur tiers précise:
        - l’identifiant du point,
        - le login de l’utilisateur
        - l’identifiant du contrat
        - qu’il dispose de l’autorisation client.

        Résultat attendu

        Code retour : SGT200 – Succès. La demande est recevable. Les historiques de consommations du point sont retournés.
        """
        res = self.service.consulter("98800007059999")
        self.assertEqual('SGT200', res['code'])

    def test_ahc_nr1(self):
        """AHC-NR1 Accès à l’historique de consommations pour un acteur tiers sans autorisation client

        Pré-requis

        Le PRM est en service.

        Descriptif

        Dans sa demande, l’acteur tiers précise:
        - l’identifiant du point,
        - le login de l’utilisateur
        - l’identifiant du contrat
        - qu’il ne dispose pas de l’autorisation client.

        Résultat attendu

        Code retour : SGT4G2 − Le demandeur n'est pas éligible à la consultation des données de mesures sur le point.
        """
        res = self.service.consulter("98800007059999", autorisation_client=0)
        self.assertEqual('Le demandeur n\'est pas éligible à la consultation des données de mesures sur le point.', res['message'])
        self.assertEqual('SGT4G2', res['code'])

class TestConsultationMesuresDetaillees(unittest.TestCase):

    def setUp(self):
        self.service = sge.ConsultationMesuresDetaillees(session)

    def test_cmd2_r1(self):
        """CMD2-R1 Accès à l’historique des courbes de puissance active au pas enregistré pour un acteur tiers avec une autorisation client

        Pré-requis

        Le PRM est en service.

        Descriptif

        Dans sa demande, l’acteur tiers précise:
        - L’identifiant du point,
        - Le login de l’utilisateur
        - Disposer de l’autorisation expresse du client
        - Si la demande concerne des points en soutirage ou en injection
        - Le type de mesure (« COURBE »)
        - La grandeur physique demandée (« PA »)
        - La date de début et de fin de la consultation des mesures
      - S’il souhaite des mesures brutes ou corrigées (uniquement brutes pour le C5 et le P4)

        Note : la consultation des courbes est disponible pour 7 jours consécutifs au maximum dans
        la limite des 24 derniers mois par rapport à la date du jour, limités à la dernière mise en
        service.

        Résultat attendu

        Code retour : La demande est recevable. L’historique de courbe de puissances active au pas enregistré du point est affiché.

        JDD

        - C1-C4 30001610071843 du 01/03/2020 au 07/03/2020
        - C5    25478147557460 du 01/03/2020 au 07/03/2020
        """
        res = self.service.consulter(
            point_id=30001610071843,
            type_code='COURBE',
            grandeur_physique='PA',
            soutirage=1,
            date_debut="01/03/2020",
            date_fin="07/03/2020")
        self.assertEqual('SGT200', res['code'])

if __name__ == '__main__':
    import sys
    unittest.main(argv=sys.argv[1:])