#!/usr/bin/env python3

import os
import zeep
import requests

class WebserviceClientFactory:

    def __init__(self, wsdl_root, login, client_certificates, client_privkey, server_certificates, homologation=False):
        self.wsdl_root = wsdl_root
        self.login = login
        self.homologation = homologation

        session = requests.Session()
        session.cert = (client_certificates, client_privkey)
        session.verify = server_certificates

        self.transport = zeep.transports.Transport(session=session)

    def make_client(self, wsdl):

        wsdl_path = os.path.join(self.wsdl_root, wsdl)
        if (not os.path.exists(wsdl_path)):
            raise RuntimeError(f"Unable to find wsdl file {wsdl} in directory {self.wsdl_root}")

        client = zeep.Client(wsdl=wsdl_path, transport=self.transport)

        if self.homologation:
            client.service._binding_options["address"] = client.service._binding_options["address"].replace(
                'https://sge-b2b.enedis.fr', 'https://sge-homologation-b2b.enedis.fr')

        return client


class RechercherPoint:

    def __init__(self, client_factory):
        self.client_factory = client_factory
        self.client = client_factory.make_client('Enedis.SGE.GUI.0427.B2B RecherchePointV2.0_v1.1/Services/RecherchePoint/RecherchePoint-v2.0.wsdl')

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

    def rechercher_point(self, criteres):
        try :
            res = self.client.service.rechercherPoint(criteres=criteres, loginUtilisateur=self.client_factory.login)
            # TODO read for _value_1 https://docs.python-zeep.org/en/master/datastructures.html#xsd-choice
            return {
                'code': res['header']['acquittement']['resultat']['code'],
                'message': res['header']['acquittement']['resultat']['_value_1'],
                'points': res['body']['points']['point'] if res['body']['points'] else []
            }
        except zeep.exceptions.Fault as fault:
            res = fault.detail[0][0]
            return {
                'code': res.attrib['code'],
                'message': res.text,
                'points': []
            }