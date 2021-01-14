# -*- coding: UTF-8 -*-
# modules : python3-zeep xmlsec

import os
import zeep
#from zeep.transports import Transport
#from requests import Session
#from requests.auth import HTTPBasicAuth
import requests
import logging.config

logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(name)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'zeep.transports': {
            'level': 'DEBUG',
            'propagate': True,
            'handlers': ['console'],
        },
    }
})

# test du shéma :
# python3 -mzeep ../../001_services_soap/Enedis.SGE.GUI.0427.B2B\ RecherchePointV2.0_v1.1/Services/RecherchePoint/RecherchePoint-v2.0.wsdl

WSDL_SCHEMA_FILE_URL = "file://" + '~/cloud.consometers.org/projets/201909_sen2/01_quoalise/lot_proxy_sge/documentation_SGE/000_homologation/001_services_soap/Enedis.SGE.GUI.0427.B2B RecherchePointV2.0_v1.1/Services/RecherchePoint/RecherchePoint-v2.0.wsdl'
#WSSE = UsernameToken("***", "***")

req_session = requests.Session()
#req_session.verify = True
#req_session.timeout = 5
req_session.auth = requests.auth.HTTPBasicAuth("***", "***")
req_session.cert = ("fullchain2.pem", "privkey2.pem")
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

result = zeep_client.service.rechercherPoint(criteres=mes_criteres, loginUtilisateur="homologation@cyrillugan.fr")
print(result)

