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

client_factory = sge.WebserviceClientFactory(wsdl_root=conf_abspath('WSDL_FILES_ROOT'),
                                             login=conf['LOGIN'],
                                             client_certificates=conf_abspath('CERT_FULLCHAIN'),
                                             client_privkey=conf_abspath('CERT_PRIVKEY'),
                                             server_certificates='./server-fullchain.pem',
                                             homologation=True)

class TestRechercherPoint(unittest.TestCase):

    def setUp(self):
        self.service = sge.RechercherPoint(client_factory)

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

        res = self.service.rechercher_point(criteres)
        self.assertEqual('SGT200', res['code'])
        self.assertTrue(len(res['points']) < 200)

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

        res = self.service.rechercher_point(criteres)
        self.assertEqual('SGT200', res['code'])
        self.assertEqual(1, len(res['points']))

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

        res = self.service.rechercher_point(criteres)
        self.assertEqual('SGT200', res['code'])
        self.assertEqual(1, len(res['points']))

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

        res = self.service.rechercher_point(criteres)
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

        res = self.service.rechercher_point(criteres)
        self.assertEqual('Les critères renseignés ne sont pas suffisants.', res['message'])
        self.assertEqual('SGT4F7', res['code'])


    def test_not_found(self):
        """Recherche d’un point inexistant

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

        res = self.service.rechercher_point(criteres)
        self.assertEqual('SGT200', res['code'])
        self.assertEqual(0, len(res['points']))

if __name__ == '__main__':
    import sys
    unittest.main(argv=sys.argv[1:])