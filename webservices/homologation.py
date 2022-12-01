#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# modules : python3-zeep

import os
import argparse
import unittest
import logging.config
import json
import datetime as dt
import csv
import sys

import sge

parser = argparse.ArgumentParser()
parser.add_argument("conf", help="Configuration file (typically private/*.conf.json)")
parser.add_argument('--report', action='store_true', help="Generate data for an homologation (does not run all unit tests)")
parser.add_argument('tests', type=str, nargs='*',
                    help='List of tests to run, like TestConsultationMesures.test_ahc_r1 for unit tests or AHC-R1 for homologation report')
args = parser.parse_args()


# Cas de tests basés sur le document
# Enedis.SGE.REF.0465.Homologation_Catalogue des cas de tests_Tiers_SGE22.1_v1.0
# Le rapport sera créé dans l’ordre des tests suivants

TEST_CASES = {
    'ConsultationDonneesTechniquesContractuelles': {
        'version': 'V1.0',
        'cases': [
            {'code': 'ADP-R1',  'prm': '98800007059999'}, #C1-C4
            {'code': 'ADP-R1',  'prm': '25946599093143'}, #C5
            {'code': 'ADP-R2',  'prm': '98800007059999'},
            {'code': 'ADP-R2',  'prm': '25946599093143'},
            {'code': 'ADP-NR1', 'prm': '99999999999999'},
        ]
    },
    'ConsultationMesures': {
        'version': 'V1.1',
        'cases': [
            {'code': 'AHC-R1',  'prm': '98800005782026'},
            {'code': 'AHC-R1',  'prm': '25957452924301'},
            {'code': 'AHC-NR1', 'prm': '98800005782026'},
        ]
    },
    'ConsultationMesuresDetaillees': {
        'version': 'V2.0',
        'cases': [
            {'code': 'CMD2-R1',  'prm': '30001610071843'},
            # {'code': 'CMD2-R1',  'prm': '25478147557460'},
            {'code': 'CMD2-R2',  'prm': '30001610071843'},
            {'code': 'CMD2-R3',  'prm': '25478147557460'},
            {'code': 'CMD2-R4',  'prm': '25478147557460'},
            {'code': 'CMD2-NR1', 'prm': '25478147557460'},
            {'code': 'CMD2-NR2', 'prm': '25478147557460'},
        ]
    },
    'RecherchePoint': {
        'version': 'V2.0',
        'cases': [
            {'code': 'RP-R1'},
            {'code': 'RP-R2'},
            {'code': 'RP-R3'},
            {'code': 'RP-NR1'},
            {'code': 'RP-NR2'}
        ]
    },
    'CommandeCollectePublicationMesures': {
        'version': 'V3.0',
        'cases': [
            {'code': 'F300C_O1', 'prm': '25884515170669'},
            # {'code': 'F300B_O1', 'prm': '98800000000246'},
            {'code': 'F300C_O2', 'prm': '25884515170669'},
            {'code': 'F300B_O2', 'prm': '98800000000246'},
            {'code': 'F305', 'prm': '25884515170669'},
            {'code': 'F305A', 'prm': '98800000000246'},
            {'code': 'F305C', 'prm': '25884515170669'},
            {'code': 'F300C_O1_NR', 'prm': '25884515170669'},
            {'code': 'F300C_O2_NR', 'prm': '25884515170669'},
            # {'code': 'F300B_O2-NR', 'prm': '98800000000246'},
            {'code': 'F305_NR', 'prm': '25884515170669'},
            # {'code': 'F305A-NR', 'prm': '98800000000246'}
        ]
    },
    'RechercheServicesSouscritsMesures': {
        'version': 'V1.0',
        'cases': [
            {'code': 'RS-R1', 'prm': '25884515170669'}
        ]
    },
    'CommandeArretServiceSouscritMesures': {
        'version': 'V1.0',
        'cases': [
            {'code': 'ASS-R1', 'prm': '25884515170669'}
        ]
    },
    'CommandeTransmissionDonneesInfraJ': {
        'version': 'V1.0',
        'cases': [
            {'code': 'F375A-R1', 'prm': '98800000000246'},
            {'code': 'F375A-NR1', 'prm': '98800000000246'}
        ]
    },
    'CommandeTransmissionHistoriqueMesures': {
        'version': 'V1.0',
        'cases': [
            {'code': 'F380-R1', 'prm': '25957452924301', 'pcdc': "30"},
            {'code': 'F380-R1', 'prm': '98800005144497', 'pcdc': "10"},
            {'code': 'F385B-R1', 'prm': '25957452924301'},
            {'code': 'F380-NR1', 'prm': '25957452924301'},
            {'code': 'F385B-NR1', 'prm': '25957452924301'}
        ]
    }
}

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
                      server_certificates='./enedis-fullchain.pem',
                      homologation=True)

class TestRecherchePoint(unittest.TestCase):

    def setUp(self):
        self.service = sge.RechercherPoint(session)

    def test_name_and_version(self, version="V2.0"):
        expected_name = type(self).__name__[4:] + version
        services = list(self.service.client.wsdl.services.values())
        self.assertEqual(expected_name, services[0].name)

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

        Code postal : 34650
        Code INSEE : 34231
        Domaine de tension : BTINF
        Catégorie du client :RES
        """

        criteres = {
            'adresseInstallation': {
                'codePostal': 34650,
                'codeInseeCommune': 34231,
                },
            'domaineTensionAlimentationCode': 'BTINF',
            'categorieClientFinalCode': 'RES'
        }

        res = self.service.rechercher(criteres)
        self.assertEqual('SGT200', res['code'])
        self.assertTrue(len(res['data']) < 200)
        return res

    def test_rp_r2(self):
        """RP-R2 Recherche du N° de PRM à partir de l’adresse et du nom exact du client pour un fournisseur non titulaire du point

        Pré-requis

        L’acteur tiers dispose d’informations n’étant pas relatives au client pour le point à rechercher.

        Descriptif

        L’acteur tiers précise dans sa demande:
        - Le code postal (84160)
        - Le code INSEE de la commune (84042)
        - L’adresse de l’installation (1 RUE DE LA MER)
        - Le nom du client (« TEST »)
        - Qu’il s’agit d’une demande de recherche d’un point en service hors du périmètre

        Résultat attendu

        La demande est recevable.
        Un unique numéro de PRM est trouvé.
        """

        criteres = {
            'adresseInstallation': {
                'codePostal': 84160,
                'codeInseeCommune': 84042,
                'numeroEtNomVoie': '1 RUE DE LA MER',
                },
            'nomClientFinalOuDenominationSociale': 'TEST',
            'rechercheHorsPerimetre': True
        }

        res = self.service.rechercher(criteres)
        self.assertEqual('SGT200', res['code'])
        self.assertEqual(1, len(res['data']))
        return res

    def test_rp_r3(self):
        """RP-R3 Recherche d’un point avec adresse exacte et nom approchant

        Pré-requis

        Recherche d’un point avec adresse exacte et nom approchant (chaîne de plus de trois caractères incluse dans le nom/dénomination sociale)

        Descriptif

        L’acteur tiers précise dans sa demande:
        - Le code postal (84160)
        - Le code INSEE de la commune (84042)
        - L’adresse de l’installation (1 RUE DE LA MER)
        - Le nom ou dénomination sociale approchant du client (« TES »)
        - Qu’il s’agit d’une demande de recherche d’un point en service hors du périmètre

        Résultat attendu

        La demande est recevable.
        Plusieurs PRM sont retournés.
        """

        criteres = {
            'adresseInstallation': {
                'codePostal': 84160,
                'codeInseeCommune': 84042,
                'numeroEtNomVoie': '1 RUE DE LA MER',
                },
            'nomClientFinalOuDenominationSociale': 'EST',
            'rechercheHorsPerimetre': True
        }

        res = self.service.rechercher(criteres)
        print(res)
        self.assertEqual('SGT200', res['code'])
        self.assertTrue(len(res['data']) > 1) #replace with > 1
        return res

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
                'codePostal': 13100,
                'codeInseeCommune': 13001,
                },
            'categorieClientFinalCode': 'PRO'
        }

        res = self.service.rechercher(criteres)
        self.assertEqual('La recherche de points renvoie trop de résultats. Veuillez affiner les critères de recherche.', res['message'])
        self.assertEqual('SGT4F8', res['code'])
        return res

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
                'codeInseeCommune': 13001,
                'numeroEtNomVoie': '16 RUE DES MENUDIERES',
            }
        }

        res = self.service.rechercher(criteres)
        self.assertEqual('Les critères renseignés ne sont pas suffisants.', res['message'])
        self.assertEqual('SGT4F7', res['code'])
        return res

class TestConsultationDonneesTechniquesContractuelles(unittest.TestCase):

    def setUp(self):
        self.service = sge.ConsultationDonneesTechniquesContractuelles(session)

    def test_name_and_version(self, version="V1.0"):
        expected_name = type(self).__name__[4:] + version
        services = list(self.service.client.wsdl.services.values())
        self.assertEqual(expected_name, services[0].name)

    def test_adp_r1(self, prm="98800007059999"):
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
        res = self.service.consulter(prm, autorisation_client=True)
        self.assertEqual('SGT200', res['code'])
        self.assertEqual(prm, res['data']['id'])
        self.assertIsNotNone(res['data']['donneesGenerales']['etatContractuel'])
        return res

    def test_adp_r2(self, prm="98800007059999"):
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
        res = self.service.consulter(prm, autorisation_client=False)
        self.assertEqual('SGT200', res['code'])
        self.assertEqual(prm, res['data']['id'])
        self.assertIsNone(res['data']['situationContractuelle'])
        return res

    def test_adp_nr1(self, prm="99999999999999"):
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
        res = self.service.consulter(prm, autorisation_client=False)
        self.assertEqual('Demande non recevable : point inexistant', res['message'])
        self.assertEqual('SGT401', res['code'])
        return res

class TestConsultationMesures(unittest.TestCase):

    def setUp(self):
        self.service = sge.ConsultationMesures(session)

    def test_name_and_version(self, version="V1.1"):
        expected_name = type(self).__name__[4:] + version
        services = list(self.service.client.wsdl.services.values())
        self.assertEqual(expected_name, services[0].name)

    def test_ahc_r1(self, prm="98800005782026"):
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
        res = self.service.consulter(prm, autorisation_client=True)
        self.assertEqual('SGT200', res['code'])
        return res

    def test_ahc_nr1(self, prm="98800005782026"):
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
        res = self.service.consulter(prm, autorisation_client=0)
        self.assertEqual('Le demandeur n\'est pas éligible à la consultation des données de mesures sur le point.', res['message'])
        self.assertEqual('SGT4G2', res['code'])
        return res

class TestConsultationMesuresDetaillees(unittest.TestCase):

    def setUp(self):
        self.service = sge.ConsultationMesuresDetaillees(session)

    def test_name_and_version(self, version="V2.0"):
        # FIXME, service name does not match, does not include version
        expected_name = "AdamConsultationMesuresServiceRead"
        services = list(self.service.client.wsdl.services.values())
        self.assertEqual(expected_name, services[0].name)

    def test_cmd2_r1(self, prm="30001610071843"):
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
        - S’il souhaite des mesures brutes ou corrigées (uniquement brutes pour le C5 et le P4)

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
            point_id=prm,
            type_code='COURBE',
            grandeur_physique='PA',
            soutirage=1,
            date_debut=dt.date(2020, 3, 8),
            date_fin=dt.date(2020, 3, 15),
            mesures_corrigees=1)

        # print(res)
        self.assertEqual(prm, res['data']['pointId'])
        self.assertTrue(len(res['data']['grandeur']) > 0)
        self.assertTrue(len(res['data']['grandeur'][0]['mesure']) > 0)
        return res

    def test_cmd2_r2(self, prm="30001610071843"):
        """CMD2-R2 Accès à l’historique des courbes de puissance réactive inductive au pas enregistré pour un acteur tiers avec une autorisation client

        Pré-requis

        Le PRM est en service.

        Descriptif

        Dans sa demande, l’acteur tiers précise:
        - L’identifiant du point,
        - Le login de l’utilisateur
        - Disposer de l’autorisation expresse du client
        - Si la demande concerne des points en soutirage ou en injection
        - Le type de mesure (« COURBE »)
        - La grandeur physique demandée (« PRI »)
        - La date de début et de fin de la consultation des mesures
       - S’il souhaite des mesures brutes ou corrigées (uniquement brutes pour le C5 et le P4)

        Note : la consultation des courbes est disponible pour 7 jours consécutifs au maximum dans
        la limite des 24 derniers mois par rapport à la date du jour, limités à la dernière mise en
        service.

        Résultat attendu

        Code retour : La demande est recevable. L’historique de courbe des puissances réactives au pas enregistré du point est affiché.
        JDD

        - C1-C4 30001610071843 du 01/03/2020 au 07/03/2020
        """
        res = self.service.consulter(
            point_id=prm,
            type_code='COURBE',
            grandeur_physique='PRI',
            soutirage=1,
            date_debut=dt.date(2020, 3, 8),
            date_fin=dt.date(2020, 3, 15),
            mesures_corrigees=1),
            
        self.assertEqual(prm, res[0]['data']['pointId'])
        self.assertTrue(len(res[0]['data']['grandeur']) > 0)
        self.assertTrue(len(res[0]['data']['grandeur'][0]['mesure']) > 0)
        return res

    def test_cmd2_r3(self, prm="25478147557460"):
        """CMD2-R3 Accès à l’historique des énergies globales quotidiennes pour un acteur tiers avec une autorisation client

        Pré-requis

        Le PRM est en service.

        Descriptif

        Dans sa demande, l’acteur tiers précise:
        - L’identifiant du point,
        - Le login de l’utilisateur
        - Disposer de l’autorisation expresse du client
        - Si la demande concerne des points en soutirage ou en injection
        - Le type de mesure (« ENERGIE »)
        - La grandeur physique demandée (« EA »)
        - La date de début et de fin de la consultation des mesures
       - S’il souhaite des mesures brutes ou corrigées (uniquement brutes pour le C5 et le P4)

        Note : la consultation des énergies globales quotidiennes est disponible sur une profondeur
        d’historique de 36 mois maximum, par rapport à la date du jour, limitée par la date de
        dernière mise en service.

        Résultat attendu

        Code retour : La demande est recevable. Les historiques d’énergies globales quotidiennes du point sont affichés.

        JDD

        - C5 25478147557460 du 01/03/2020 au 07/03/2020
        """
        res = self.service.consulter(
            point_id=prm,
            type_code='ENERGIE',
            grandeur_physique='EA',
            soutirage=1,
            date_debut=dt.date(2020, 3, 1),
            date_fin=dt.date(2020, 3, 7),
            mesures_corrigees=0)


        self.assertEqual(prm, res['data']['pointId'])
        self.assertTrue(len(res['data']['grandeur']) > 0)
        self.assertTrue(len(res['data']['grandeur'][0]['mesure']) > 0)
        return res



    def test_cmd2_r4(self, prm="25478147557460"):
        """CMD2-R4 Accès à l’historique de puissances maximales quotidiennes ou mensuelles pour un acteur tiers avec une autorisation client

        Pré-requis

        Le PRM est en service.

        Descriptif

        Dans sa demande, l’acteur tiers précise:
        - L’identifiant du point,
        - Le login de l’utilisateur
        - Disposer de l’autorisation expresse du client
        - Si la demande concerne des points en soutirage ou en injection
        - Le type de mesure (« PMAX »)
        - La grandeur physique demandée (« PMA »)
        - Le pas souhaité (P1D pour un pas quotidien, P1M pour un pas mensuel)
        - La date de début et de fin de la consultation des mesures
       - S’il souhaite des mesures brutes ou corrigées (uniquement brutes pour le C5 et le P4)

        Note : la consultation des puissances maximales quotidiennes est disponible sur une
        profondeur d’historique de 36 mois maximum, par rapport à la date du jour, limitée par la
        date de dernière mise en service.

        Résultat attendu

        Code retour : La demande est recevable. Les historiques des puissances maximales quotidiennes ou mensuelles du point sont affichés.

        JDD

        - C5 25478147557460 du 01/01/2020 au 01/02/2020
        """
        res = self.service.consulter(
            point_id=prm,
            type_code='PMAX',
            grandeur_physique='PMA',
            soutirage=1,
            date_debut=dt.date(2020, 1, 1),
            date_fin=dt.date(2020, 2, 1),
            mesures_corrigees= 0,
            mesures_pas="P1D")

        self.assertEqual(prm, res['data']['pointId'])
        self.assertTrue(len(res['data']['grandeur']) > 0)
        self.assertTrue(len(res['data']['grandeur'][0]['mesure']) > 0)
        return res

    def test_cmd2_nr1(self, prm="25478147557460"):
        """CMD2-NR2 Accès à l’historique de courbe de puissance active dont la profondeur maximale (7 jours) n’est pas respectée

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
        - Une date de début et de fin ne respectant pas la profondeur maximale de 7 jours
       - S’il souhaite des mesures brutes ou corrigées (uniquement brutes pour le C5 et le P4)

        Résultat attendu

        Code retour : SGT4L8 – La durée demandée n’est pas compatible avec le type de mesure demandé
        La demande est non passante car l’acteur tiers a demandé une profondeur d’historique de
        courbe dépassant les 7 jours autorisés pour ce service.

        JDD

        - C5 25478147557460 du 01/01/2020 au 09/01/2020
        """
        res = self.service.consulter(
            point_id=prm,
            type_code='COURBE',
            grandeur_physique='PA',
            soutirage=1,
            mesures_corrigees= 0,
            date_debut=dt.date(2020, 1, 1),
            date_fin=dt.date(2020, 1, 9))

        self.assertEqual('La durée demandée n’est pas compatible avec le type de mesure demandé', res['message'])
        self.assertEqual('SGT4L8', res['code'])
        return res

    def test_cmd2_nr2(self, prm="25478147557460"):
        """CMD2-NR2 Accès à l’historique des énergies globales quotidiennes d’un point pour un acteur tiers sans autorisation client

        Pré-requis

        Le PRM est en service.

        Descriptif

        Dans sa demande, l’acteur tiers précise:
        - L’identifiant du point,
        - Le login de l’utilisateur
        - Ne pas disposer de l’autorisation du client
        - Si la demande concerne des points en soutirage ou en injection
        - Le type de mesure (« ENERGIE »)
        - La grandeur physique demandée (« EA »)
        - La date de début et de fin de la consultation des mesures
       - S’il souhaite des mesures brutes ou corrigées (uniquement brutes pour le C5 et le P4)

        Résultat attendu

        Code retour : SGT4K2 – Le client doit avoir donné son accord pour la transmission de ses données de mesure.
        La demande est non recevable car l’acteur tiers doit avoir l’accord du client pour accéder aux données.

        JDD

        - C5 25478147557460 du 01/01/2020 au 07/01/2020
        """
        res = self.service.consulter(
            point_id=prm,
            type_code='ENERGIE',
            grandeur_physique='EA',
            soutirage=1,
            mesures_corrigees=0,
            date_debut=dt.date(2020, 1, 1),
            date_fin=dt.date(2020, 1, 9),
            accord_client=0)

        self.assertEqual('Le client doit avoir donné son accord pour la transmission de ses données de mesure.', res['message'])
        self.assertEqual('SGT4K2', res['code'])
        return res

class TestCommandeCollectePublicationMesures(unittest.TestCase):

    def setUp(self):
        self.service = sge.CommandeCollectePublicationMesures(session)

    def test_name_and_version(self, version="V3.0"):
        expected_name = "CommandeCollectePublicationMesures-V3.0"
        services = list(self.service.client.wsdl.services.values())
        self.assertEqual(expected_name, services[0].name)

    def test_f300c_o1(self, prm="25884515170669"):
        """F300C_O1 Demande de transmission récurrente de courbe de charge

        Pré-requis

        Le PRM est en service.
        Pour les points du segment C2-C4, le compteur doit être compatible (ICE, PMEPMI, SAPHIR télérelevés).
        Pour les points du segment C5, le compteur Linky doit être de niveau 2.

        Descriptif

        L'acteur tiers demande la transmission récurrente de la courbe de charge.
        - Le type de mesure demandé doit être CDC
        - La confirmation de possession du consentement client pour toute la durée du service doit être renseignée.

        Précisions C5
        - La date de début du service doit être égale à la date du jour.
        - La fréquence de publication souhaitée peut être quotidienne ou mensuelle
        - La date souhaitée de fin du service doit être dans les 12 mois suivant la date de début (la durée du service ne peut excéder un an).

        Résultat attendu

        Code retour : SGT200 – Succès. La demande est recevable. L'affaire est créée. Le bloc "prestations" est renvoyé.
        Si le même service est souscrit sur le PRM, SGE retourne le code SGT570 - Le service est déjà actif sur la période demandée.
        
        La souscription au service de transmission récurrente de courbe de charge est réalisée sur le PRM.

        JDD

        - C5 25884515170669
        """

        
        res = self.service.consulter(
            point_id=prm,
            objet_code='AME',
            soutirage=1,
            mesure_type_code='CDC',
            mesure_pas='PT30M',
            transmission_recurrente=1,
            periodicite_transmission='P1M',
            mesures_corrigees=0,
            date_debut=dt.date.today(),
            date_fin=dt.date(2022, 12, 31))

        # print(res)
        if res['data']['header']['acquittement']['resultat']['code'] == 'SGT200':
            self.assertTrue(len(res['data']['body']['prestations']) > 0)
            self.assertTrue(res['data']['body']['prestations']['prestation'][0]['option']['code'] == 'F300CO1')
        else:
            self.assertEqual('SGT570', res['code'])
        return res

    def test_f300c_o2(self, prm="25884515170669"):
        """F300C_O2 Demande de collecte de la courbe de charge

        Pré-requis

        Le PRM est en service.
        Pour les points du segment C2-C4, le compteur doit être compatible (ICE, PMEPMI, SAPHIR télérelevés).
        Pour les points du segment C5, le compteur Linky doit être de niveau 2.

        Descriptif

        L'acteur tiers demande la collecte de la courbe de charge.
        - Le type de mesure demandé doit être CDC
        - La confirmation de possession du consentement client pour toute la durée du service doit être renseignée.
        - La balise "transmissionRecurrente" doit être renseignée à false.

        Précisions C5
        - La date de début du service doit être égale à la date du jour.
        - La date souhaitée de fin du service doit être dans les 12 mois suivant la date de début (la durée du service ne peut excéder un an).

        Résultat attendu

        Code retour : SGT200 – Succès. La demande est recevable. L'affaire est créée. Le bloc "prestations" est renvoyé.
        Si le même service est souscrit sur le PRM, SGE retourne le code SGT570 - Le service est déjà actif sur la période demandée.
        
        La souscription au service de transmission récurrente de courbe de charge est réalisée sur le PRM.

        JDD

        - C5 25884515170669
        """

        
        res = self.service.consulter(
            point_id=prm,
            objet_code='AME',
            soutirage=1,
            mesure_type_code='CDC',
            mesure_pas='PT30M',
            transmission_recurrente=0,
            periodicite_transmission='P1M',
            mesures_corrigees=0,
            date_debut=dt.date.today(),
            date_fin=dt.date(2022, 12, 31))

        # print(res)
        if res['code'] == 'SGT200':
            self.assertTrue(len(res['data']['body']['prestations']) > 0)
            self.assertTrue(res['data']['body']['prestations']['prestation'][0]['option']['code'] == 'F300CO2')
        else:
            self.assertEqual('SGT570', res['code'])
        return res

    def test_f300b_o2(self, prm="98800000000246"):
        """F300B_O2 Demande de collecte de la courbe de charge

        Pré-requis

        Le PRM est en service.
        Pour les points du segment C2-C4, le compteur doit être compatible (ICE, PMEPMI, SAPHIR télérelevés).
        Pour les points du segment C5, le compteur Linky doit être de niveau 2.

        Descriptif

        L'acteur tiers demande la collecte de la courbe de charge.
        - Le type de mesure demandé doit être CDC
        - La confirmation de possession du consentement client pour toute la durée du service doit être renseignée.
        - La balise "transmissionRecurrente" doit être renseignée à false.

        Précisions C5
        - La date de début du service doit être égale à la date du jour.
        - La date souhaitée de fin du service doit être dans les 12 mois suivant la date de début (la durée du service ne peut excéder un an).

        Résultat attendu

        Code retour : SGT200 – Succès. La demande est recevable. L'affaire est créée. Le bloc "prestations" est renvoyé.
        Si le même service est souscrit sur le PRM, SGE retourne le code SGT570 - Le service est déjà actif sur la période demandée.
        
        La souscription au service de transmission récurrente de courbe de charge est réalisée sur le PRM.

        JDD

        - C5 25884515170669
        """

        
        res = self.service.consulter(
            point_id=prm,
            objet_code='AME',
            soutirage=1,
            mesure_type_code='CDC',
            mesure_pas='PT10M',
            transmission_recurrente=0,
            periodicite_transmission='P1M',
            mesures_corrigees=0,
            date_debut=dt.date.today(),
            date_fin=dt.date(2022, 12, 31))

        print(res)
        if res['code'] == 'SGT200':
            self.assertTrue(len(res['data']['body']['prestations']) > 0)
            self.assertTrue(res['data']['body']['prestations']['prestation'][0]['option']['code'] == 'F300CO2')
        else:
            self.assertEqual('SGT570', res['code'])
        return res


    def test_f305(self, prm="25884515170669"):
        """F305 Demande de transmission récurrente des index quotidiens et puissances maximales quotidiennes

        Pré-requis

        Le PRM est en service.

        Descriptif

        L'acteur tiers demande la transmission récurrente des index quotidiens et des puissances maximales quotidiennes.

        - Le type de mesure demandé doit être IDX
        - La confirmation de possession du consentement client pour toute la durée du service doit être renseignée.
        - La fréquence de transmission doit être renseignée
        - La date de début du service doit être égale à la date du jour.
        - La date souhaitée de fin du service doit être dans les 12 mois suivant la date de début (la durée du service ne peut excéder un an).

        Résultat attendu

        Code retour : SGT200 – Succès. La demande est recevable. L'affaire est créée. Le bloc "prestations" est renvoyé.
        Si le même service est souscrit sur le PRM, SGE retourne le code SGT570 - Le service est déjà actif sur la période demandée.
        
        La souscription au service de transmission récurrente des index quotidiens et puissances maximales quotidiennes est réalisée sur le PRM.

        JDD

        - C5 25884515170669
        """

        
        res = self.service.consulter(
            point_id=prm,
            objet_code='AME',
            soutirage=1,
            mesure_type_code='IDX',
            mesure_pas='P1D',
            transmission_recurrente=1,
            periodicite_transmission='P1D',
            mesures_corrigees=0,
            date_debut=dt.date.today(),
            date_fin=dt.date(2022, 12, 31))

        # print(res)
        if res['data']['header']['acquittement']['resultat']['code'] == 'SGT200':
            self.assertTrue(len(res['data']['body']['prestations']) > 0)
            self.assertTrue(res['data']['body']['prestations']['prestation'][0]['fiche']['code'] == 'F305')
        else:
            self.assertEqual('SGT570', res['code'])
        return res 

    def test_f305a(self, prm="98800000000246"):
        """F305A Demande de transmission des index quotidiens et autres données du compteur

        Pré-requis

        Le PRM est en service.
        Le compteur doit être compatible (ICE, PMEPMI, SAPHIR rélérelevés)

        Descriptif

        L'acteur tiers demande la transmission des index J+1 et autres données du compteur.

        - Le type de mesure demandé doit être IDX
        - La confirmation de possession du consentement client pour toute la durée du service doit être renseignée.
        - La fréquence de transmission doit être quotidienne
        - La date de début du service doit être postérieure ou égale à la date du jour.
        - La balise "transmissionRecurrente" renseignée à true
        - La balise "soutirage" renseignée à true, celle "d'injection" à false


        Note : Pour commander une prestation P3005A la balise soutirage doit être à false et injection à true.

        Résultat attendu

        Code retour : SGT200 – Succès. La demande est recevable. L'affaire est créée. Le bloc "prestations" est renvoyé.
        Si le même service est souscrit sur le PRM, SGE retourne le code SGT570 - Le service est déjà actif sur la période demandée.
        
        La souscription au service de transmission des index J+1 et autres données du compteur est réalisée sur le PRM.

        JDD

        - C2-C4 98800000000246
        """

        
        res = self.service.consulter(
            point_id=prm,
            objet_code='AME',
            soutirage=1,
            injection=0,
            mesure_type_code='IDX',
            mesure_pas='P1D',
            transmission_recurrente=1,
            periodicite_transmission='P1D',
            mesures_corrigees=0,
            date_debut=dt.date.today(),
            date_fin=dt.date(2022, 12, 31)) # end date is optional for C1-C4 P1-P3

        print(res)
        if res['data']['header']['acquittement']['resultat']['code'] == 'SGT200':
            self.assertTrue(len(res['data']['body']['prestations']) > 0)
            self.assertTrue(res['data']['body']['prestations']['prestation'][0]['fiche']['code'] == 'F305A')
        else:
            self.assertEqual('SGT570', res['code'])
        return res


    def test_f305c(self, prm="25884515170669"):
        """F305C Demande de renouvellement d'un service de transmission récurrente des index quotidiens et puissances maximales quotidiennes

        Pré-requis

        Le PRM est en service.
        L'acteur tiers a souscrit un service F305 sur le PDL et ce service est toujours actif.

        Descriptif

        L'acteur tiers demande le renouvellement du service de transmission récurrente des index quotidiens et des puissances maximales quotidiennes. Les balises indiquées lors du renouvellement doivent obligatoirement être identique à celles de la demande initiale du service.

        - Le type de mesure demandé doit être IDX
        - La récurrence et la fréquence de transmission doivent être renseignées.
        - La date de début du renouvellement doit être égale à la date du jour
        - La date de fin souhaitée du renouvellement doit être postérieure à la date de fin du premier service souscrit.
        - La date souhaitée de fin du renouvellement doit être dans les 12 mois suivants la date du début du renouvellement (la durée du service ne peut excéder un an).
        La confirmation de possession du consentement client pour toute la durée du service doit être renseignée.

        Résultat attendu

        Code retour : SGT200 – Succès. La demande est recevable. L’affaire est créée. Le bloc « prestations » est renvoyé.
        L’extension de la date de fin du service de demande de transmission récurrente des index quotidiens et puissances maximales est réalisée sur le PDL.

        JDD

        - C5 25884515170669
        """

        
        res = self.service.consulter(
            point_id=prm,
            objet_code='AME',
            soutirage=1,
            mesure_type_code='IDX',
            mesure_pas='P1D',
            transmission_recurrente=1,
            periodicite_transmission='P1D',
            mesures_corrigees=0,
            date_debut=dt.date.today(),
            date_fin=dt.date(2023, 1, 2))

        print(res)
        if res['data']['header']['acquittement']['resultat']['code'] == 'SGT200':
            self.assertTrue(len(res['data']['body']['prestations']) > 0)
            self.assertTrue(res['data']['body']['prestations']['prestation'][0]['fiche']['code'] == 'F305')
        else:
            self.assertEqual('SGT570', res['code'])
        return res 

    def test_f300c_o1_nr(self, prm="25884515170669"):
        """F300C-O1-NR Demande de transmission récurrente de courbe de charge, sur une période supérieure à 12 mois

        Pré-requis

        Le PRM est en service.

        Descriptif

        L’acteur tiers demande la transmission récurrente de la courbe de charge. La date souhaitée de fin du service est supérieure à 12 mois vis-à-vis de la date de début.

        - Le type de mesure demandé doit être CDC
        - La date de début doit être égale à la date du jour
        - La confirmation de possession du consentement client pour toute la durée du service doit être renseignée.
        - La récurrence et la fréquence de transmission doivent être renseignées

        Résultat attendu

        Code retour : SGT4H4 – La date de fin doit être renseignée et la durée demandée pour l'accès aux données de mesures ne doit pas excéder 1 an.
        La demande est non recevable, la période entre la date de début et la date de fin du service doit être inférieure ou égale à 12 mois.

        JDD

        - C5 25884515170669
        """

        
        res = self.service.consulter(
            point_id=prm,
            objet_code='AME',
            soutirage=1,
            mesure_type_code='CDC',
            mesure_pas='PT30M',
            transmission_recurrente=1,
            periodicite_transmission='P1D',
            mesures_corrigees=0,
            date_debut=dt.date.today(),
            date_fin=dt.date(2024, 1, 2))

        # print(res)
        self.assertEqual('SGT4H4', res['code'])
        return res


    def test_f300c_o2_nr(self, prm="25884515170669"):
        """F300C-O2-NR Demande de collecte de la courbe de charge sans autorisation client.

        Pré-requis

        Le PRM est en service.

        Descriptif

        L’acteur tiers demande la transmission récurrente de la courbe de charge. La date souhaitée de fin du service est supérieure à 12 mois vis-à-vis de la date de début.

        - Le type de mesure demandé doit être CDC
        - L'autoristation du client n'est pas confirmée
        - Le souhait d’activer uniquement la collecte de la courbe de charge doit être renseigné.
        - La date de début du service doit être égale à la date du jour.
        - La date souhaitée de fin du service doit être dans les 12 mois suivant la date de début (la durée du service ne peut excéder un an)

        Résultat attendu

        Code retour : SGT566 – Ce service nécessite l'accord du client. La demande est non recevable car l’accord client n’est pas confirmé.

        JDD

        - C5 25884515170669
        """

        
        res = self.service.consulter(
            point_id=prm,
            objet_code='AME',
            soutirage=1,
            mesure_type_code='CDC',
            mesure_pas='PT30M',
            transmission_recurrente=1,
            periodicite_transmission='P1D',
            mesures_corrigees=0,
            accord_client=0,
            date_debut=dt.date.today(),
            date_fin=dt.date(2024, 1, 2))

        # print(res)
        self.assertEqual('SGT566', res['code'])
        return res


    def test_f305_nr(self, prm="25884515170669"):
        """F305-NR Demande de transmission récurrente des index quotidiens sans autorisation client.

        Pré-requis

        Le PRM est en service.

        Descriptif

        L'acteur tiers demande la transmission récurrente des index quotidiens et des puissances maximales quotidiennes.

        - Le type de mesure demandé doit être IDX
        - La confirmation de possession du consentement client pour toute la durée du service doit être renseignée.
        - La fréquence de transmission doit être renseignée
        - La date de début du service doit être égale à la date du jour.
        - La date souhaitée de fin du service doit être dans les 12 mois suivant la date de début (la durée du service ne peut excéder un an).

        Résultat attendu

        Code retour : SGT566 – Ce service nécessite l'accord du client. La demande est non recevable car l’accord client n’est pas confirmé.

        JDD

        - C5 25884515170669
        """

        
        res = self.service.consulter(
            point_id=prm,
            objet_code='AME',
            soutirage=1,
            mesure_type_code='IDX',
            mesure_pas='P1D',
            transmission_recurrente=1,
            periodicite_transmission='P1D',
            mesures_corrigees=0,
            accord_client=0,
            date_debut=dt.date.today(),
            date_fin=dt.date(2022, 12, 31))

        # print(res)
        self.assertEqual('SGT566', res['code'])
        return res


class TestRechercheServicesSouscritsMesures(unittest.TestCase):

    def setUp(self):
        self.service = sge.RechercheServicesSouscritsMesures(session)

    def test_name_and_version(self, version="V1.0"):
        expected_name = "RechercheServicesSouscritsMesures-V1.0"
        services = list(self.service.client.wsdl.services.values())
        self.assertEqual(expected_name, services[0].name)

    def test_rs_r1(self, prm="25884515170669"):
        """RS-R1 Recherche des services souscrits sur un PRM

        Pré-requis

        L’acteur tiers dispose du numéro du PRM.
        
        Descriptif

        L’acteur tiers précise dans sa demande:
        - Le login de l’initiateur de la demande
        - l’identifiant du point
        - l’identifiant du contrat

        Résultat attendu

        Code retour : SGT200 – Succès. La demande est recevable. Le message retour contient soit :
        - La liste des services souscrits du demandeur sur le point en question et leur état
        - Un message vide si aucun service souscrit n’a été demandé par l’acteur sur le point en question

        JDD

        - C5 25884515170669
        """

        res = self.service.rechercher(prm)

        print(res)
        if res['code'] == 'SGT200':
            self.assertTrue(len(res['data']['body']['servicesSouscritsMesures']['serviceSouscritMesures']) > 0)
        return res

class TestCommandeArretServiceSouscritMesures(unittest.TestCase):

    def setUp(self):
        self.service = sge.CommandeArretServiceSouscritMesures(session)

    def test_name_and_version(self, version="V1.0"):
        expected_name = "CommandeArretServiceSouscritMesures-V1.0"
        services = list(self.service.client.wsdl.services.values())
        self.assertEqual(expected_name, services[0].name)

    def test_ass_r1(self, prm="25884515170669"):
        """ass_r1 Demande d’arrêt d’un service souscrit pour un acteur tiers titulaire du service

        Pré-requis

        Le PRM est en service. Le demandeur a préalablement souscrit à un service.        
        
        Descriptif

        L’acteur tiers précise dans sa demande :
        - Le login de l’initiateur de la demande,
        - l’identifiant du point,
        - l’identifiant du contrat,
        - l’identifiant du service souscrit.

        Résultat attendu

        Code retour : SGT200 – Succès. La demande est recevable. Le service souscrit est résilié.

        JDD

        - C5 25884515170669
        """

        
        res = self.service.consulter(point_id=prm, service_souscrit_id=47761827)

        # print(res)
        if res['code'] == 'SGT200':
            self.assertTrue(len(res['data']['body']['prestations']['prestation']) > 0)
        return res


class TestCommandeTransmissionDonneesInfraJ(unittest.TestCase):

    def setUp(self):
        self.service = sge.CommandeTransmissionDonneesInfraJ(session)

    def test_name_and_version(self, version="V1.0"):
        expected_name = "CommandeTransmissionDonneesInfraJ-V1.0"
        services = list(self.service.client.wsdl.services.values())
        self.assertEqual(expected_name, services[0].name)

    def test_f375a_r1(self, prm="98800000000246"):
        """f375a_r1 Demande de transmission de données infra-journalières avec autorisation client

        Pré-requis

        Le PRM est en service        
        
        Descriptif

        L'acteur tiers demande la transmission des données infra-journalières sur un PRM en précisant :
        - Le code objet "AME"
        - L'identifiant du contrat
        - Au moins une des balises IDX, PTD, CDC doit etre à true
        - La confirmation de possession du consentement client en soutirage


        Résultat attendu

        Code retour : SGT200 – Succès. La demande est recevable. L'affaire est créée.

        JDD

        - C5 98800000000246
        """

        
        res = self.service.consulter(point_id=prm, soutirage_accord=1)

        print(res)
        if res['code'] == 'SGT200':
            self.assertTrue(res['data']['body']['prestations']['prestation'] > 0)
        return res

    def test_f375a_nr1(self, prm="98800000000246"):
        """f375a_nr1 Demande de transmission de données infra-journalières sans autorisation client

        Pré-requis

        Le PRM est en service        
        
        Descriptif

        L'acteur tiers demande la transmission des données infra-journalières sur un PRM en précisant :
        - Le code objet "AME"
        - L'identifiant du contrat
        - Au moins une des balises IDX, PTD, CDC doit etre à true
        - L'autorisation du client par soutirage n'est pas confirmée


        Résultat attendu

        Code retour : SGT566 – Ce service nécessite l'accord du client. La demande est non recevable car l'accord client n'est pas confirmé.
        
        JDD

        - C5 98800000000246
        """

        
        res = self.service.consulter(point_id=prm, accord_client=0, soutirage_accord=0)

        print(res)
        # self.assertEqual('SGT566', res['code'])
        self.assertEqual('SGT500', res['code'])
        return res


class TestCommandeTransmissionHistoriqueMesures(unittest.TestCase):

    def setUp(self):
        self.service = sge.CommandeTransmissionHistoriqueMesures(session)

    def test_name_and_version(self, version="V1.0"):
        expected_name = "commanderTransmissionHistoriqueMesures-v1"
        services = list(self.service.client.wsdl.services.values())
        self.assertEqual(expected_name, services[0].name)

    def test_f380_r1(self, prm="98800000000246", pcdc=10):
        """f380_r1 Demande de transmission d’historique de courbe de charge pour un acteur tiers avec une autorisation client

        Pré-requis

        Le PRM est en service        
        
        Descriptif


        Résultat attendu

        Code retour : SGT200 – Succès. La demande est recevable. L'affaire est créée.

        JDD

        - C5 98800000000246
        """

        
        res = self.service.consulter(
            point_id=prm,
            mesure_type_code='CDC',
            mesures_corrigees=0,
            pas_cdc=30,
            date_debut=dt.date(2021, 1, 2),
            date_fin=dt.date(2022, 1, 2))

        print(res)
        if res['code'] == 'SGT200':
            self.assertTrue(res['data']['body']['prestations']['prestation'][0]['fiche']['code'] == 'F380')
        return res

    def test_f385b_r1(self, prm="25957452924301"):
        """f385b_r1 Demande de transmission d’historique d’index quotidiens pour un acteur tiers avec une autorisation client

        Pré-requis

        Le PRM est en service        
        
        Descriptif


        Résultat attendu

        Code retour : SGT200 – Succès. La demande est recevable. L'affaire est créée.

        JDD

        - C5 25957452924301
        """

        
        res = self.service.consulter(
            point_id=prm,
            mesure_type_code='IDX',
            mesures_corrigees=0,
            pas_cdc=30,
            date_debut=dt.date(2021, 1, 2),
            date_fin=dt.date(2022, 1, 2))

        print(res)
        self.assertTrue(res['code'] == 'SGT200')
        return res

    def test_f380_nr1(self, prm="25957452924301"):
        """f380_nr1 Demande de transmission d’historique de courbe de charge dont la profondeur maximale de 24 mois n’est pas respectée

        Pré-requis

        Le PRM est en service      
        La collecte de la courbe de charge est activée.  
        
        Descriptif
        • Disposer de l’autorisation client.
        • La date de début de l’historique de mesures doit être renseignée.
        • La date de fin de l’historique de mesures doit être renseignée.
        • La profondeur des données demandées dépasse 24 mois.
        • Le type de mesure doit être « CDC».
        • S’il souhaite des mesures brutes ou corrigées (uniquement brutes pour le C5).
        • Le pas de courbe de charge :
        - 10 min pour les points C1 – C4

        Résultat attendu

        Code retour : SGT4L8 – La durée demandée n'est pas compatible avec le type de mesure demandé.
        La demande est non recevable, la période entre la date de début et la date de fin du service doit être inférieure ou égale à 24 mois.
        JDD

        - C5 25957452924301
        """

        
        res = self.service.consulter(
            point_id=prm,
            mesure_type_code='CDC',
            mesures_corrigees=0,
            pas_cdc=30,
            date_debut=dt.date(2018, 1, 2),
            date_fin=dt.date(2022, 1, 2))

        print(res)
        self.assertTrue(res['code'] == 'SGT4L8')
        return res

    def test_f385b_nr1(self, prm="25957452924301"):
        """f385b_nr1 Demande de transmission d’historique d’index quotidiens d’un point avec une date de début à plus de 36 mois

        Pré-requis

        Le PRM est en service        
        
        Descriptif

        • Disposer de l’autorisation client.
        • La date de début de l’historique de mesures doit être renseignée.
        • La date de fin de l’historique de mesures doit être renseignée.
        • Le type de mesure doit être « IDX».

        Résultat attendu

        Code retour : SGT4L8 – La durée demandée n'est pas compatible avec le type de mesure demandé.
        La demande est non recevable, la période entre la date de début et la date de fin du service doit être inférieure ou égale à 36 mois.

        JDD

        - C5 25957452924301
        """

        
        res = self.service.consulter(
            point_id=prm,
            mesure_type_code='IDX',
            mesures_corrigees=0,
            pas_cdc=30,
            date_debut=dt.date(2018, 1, 2),
            date_fin=dt.date(2022, 1, 2))

        print(res)
        self.assertTrue(res['code'] == 'SGT4L8')
        return res

def run_test_with_args(webservice_name, test_name=None, test_code=None, arguments={}):

    test_class_name = "Test" + webservice_name
    test_class = getattr(sys.modules[__name__], test_class_name, None)
    if test_class is None:
        raise RuntimeError(test_class_name + " is not defined")

    test_case = test_class()

    if test_name is None:
        test_name = 'test_' + test_code.lower().replace('-', '_')

    test_method = getattr(test_case, test_name, None)

    if test_method is None:
        raise RuntimeError(test_class_name + "." + test_name + " is not defined")

    test_case.setUp()
    return test_method(**arguments)

def make_homologation_report(only_those_cases=None):
    errors = []
    output = csv.writer(sys.stdout)

    for webservice, params in TEST_CASES.items():

        run_test_with_args(webservice,
                           test_name='test_name_and_version',
                           arguments={'version': params['version']})

        for case in params['cases']:
            args = case.copy()
            code = args.pop('code')
            if only_those_cases and not (code in only_those_cases):
                continue
            try:
                res = run_test_with_args(webservice, test_code=code, arguments=args)
                if res != None:
                    output_name = [code]
                    output_name += [name + value for name, value in args.items()]
                    output_name = "_".join(output_name)
                    output_name = os.path.join('test_case_outputs', output_name + '.txt')
                    os.makedirs(os.path.dirname(output_name), exist_ok=True)
                    with open(output_name, 'w+') as f:
                        f.write(str(res))
                date = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            except AssertionError as e:
                date = "FAIL"
                errors.append({'webservice': webservice, 'code': code, 'error': e})
            output.writerow([webservice, code, date, repr(args)])

    for error in errors:
        sys.stderr.write(f"--------\n")
        sys.stderr.write(f"{error['code']} FAILED ({error['webservice']})\n")
        sys.stderr.write(str(error['error']))


if __name__ == '__main__':
    import sys

    if args.report:
        make_homologation_report(set(args.tests))
    else:
        unittest.main(argv=sys.argv[1:])