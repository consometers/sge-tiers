#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# modules : python3-zeep

import os
import zeep
import requests
import logging.config
import argparse
import json

parser = argparse.ArgumentParser()

parser.add_argument("conf", help="Configuration file (typically private/*.conf.json)")

args = parser.parse_args()

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

logging.basicConfig()
debug = []

#debug.append("urllib3")
#debug.append("zeep.wsdl")
debug.append("zeep.transports")

for logger in debug:
    logger = logging.getLogger(logger)
    logger.setLevel(logging.DEBUG)
    logger.propagate = True

# test du shéma :
# python3 -mzeep ../../001_services_soap/Enedis.SGE.GUI.0427.B2B\ RecherchePointV2.0_v1.1/Services/RecherchePoint/RecherchePoint-v2.0.wsdl

WSDL_SCHEMA_FILE_URL = "file://" + conf_abspath('WSDL_SCHEMA_FILE')

req_session = requests.Session()
req_session.auth = requests.auth.HTTPBasicAuth(conf['LOGIN'], conf['PASSWORD'])

req_session.cert = (conf_abspath("CERT_FULLCHAIN"),
                    conf_abspath("CERT_PRIVKEY"))

# Made with cat cat enedis-cert.pem SSL\ OV_Quovadis/intermdiaire/QuoVadis_OV_SSL_ICA_G3.pem  SSL\ OV_Quovadis/racine/QuoVadis_Root_CA_2_G3.pem > enedis-fullchain.pem
req_session.verify = './enedis-fullchain.pem'

transport_with_basic_auth_and_cert = zeep.transports.Transport(session = req_session)

zeep_client = zeep.Client(wsdl = WSDL_SCHEMA_FILE_URL, transport=transport_with_basic_auth_and_cert)

# Forcer l'URL pour l'homologation (remplace celle fournie dans le WSDL)
zeep_client.service._binding_options["address"] = 'https://sge-homologation-b2b.enedis.fr/RecherchePoint/v2.0'


# Test RP-R2 :
# L’acteur tiers précise dans sa demande:
# - Le code postal (83380)
# - Le code INSEE de la commune (83107)
# - L’adresse de l’installation (404 RUE DES CIMBRES)
# - Le nom du client (Homologation)
# Qu’il s’agit d’une demande de recherche d’un

# ns0:CriteresType(
#     adresseInstallation: ns0:AdresseInstallationType,
#          ns0:AdresseInstallationType(
#             escalierEtEtageEtAppartement: ns2:AdresseAfnorLigneType,
#             batiment: ns2:AdresseAfnorLigneType,
#             numeroEtNomVoie: ns2:AdresseAfnorLigneType,
#             lieuDit: ns2:AdresseAfnorLigneType,
#             codePostal: ns2:CodePostalFrancaisType,
#             codeInseeCommune: ns2:CommuneFranceCodeInseeType
#             )
#     numSiret: ns2:EtablissementNumSiretType,
#     matriculeOuNumeroSerie: ns2:Chaine255Type,
#     domaineTensionAlimentationCode: ns2:DomaineTensionCodeType,
#     nomClientFinalOuDenominationSociale: ns2:Chaine255Type,
#     categorieClientFinalCode: ns2:ClientFinalCategorieCodeType,
#     rechercheHorsPerimetre: xsd:boolean)

mes_criteres = {
    'adresseInstallation': {
        'codePostal': 83380,
        'codeInseeCommune': 83107,
        'numeroEtNomVoie': '404 RUE DES CIMBRES',
        },
    'nomClientFinalOuDenominationSociale': 'Homologation',
    'rechercheHorsPerimetre': True
    }

# (criteres: CriteresType, loginUtilisateur: , _soapheaders={entete: entete()}) -> body: RechercherPointResponseType, header: {acquittement: acquittement()}

result = zeep_client.service.rechercherPoint(criteres=mes_criteres, loginUtilisateur=conf['LOGIN'])

print(result)
