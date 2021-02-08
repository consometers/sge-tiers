#!/usr/bin/env python3

import os
import zeep
import requests
import logging
import re
import datetime as dt
import time
import threading

class Session:

    def __init__(self, wsdl_root, login, contract_id, client_certificates, client_privkey, server_certificates, homologation=False):
        self.wsdl_root = wsdl_root
        self.login = login
        self.homologation = homologation
        self.contract_id = contract_id
        self.logger = logging.getLogger('sge')

        session = requests.Session()
        session.cert = (client_certificates, client_privkey)
        session.verify = server_certificates

        self.transport = zeep.transports.Transport(session=session)

        # It is forbidden to call webservices more than once / sec in homologation
        # TODO add to docs
        # TODO check limit for non homologation
        self.throttle = Throttle(1.0)

    def make_client(self, wsdl):

        wsdl_path = os.path.join(self.wsdl_root, wsdl)
        if (not os.path.exists(wsdl_path)):
            raise RuntimeError(f"Unable to find wsdl file {wsdl} in directory {self.wsdl_root}")

        client = zeep.Client(wsdl=wsdl_path, transport=self.transport)

        if self.homologation:
            address = client.service._binding_options["address"]
            address = re.sub(r'^https://[^/]+/', 'https://sge-homologation-b2b.enedis.fr/', address)
            client.service._binding_options["address"] = address

        return client

class Throttle:

    def __init__(self, time_between_calls, time_provider=time.monotonic):
        self.time_between_calls = time_between_calls
        self.time_provider = time_provider
        self.next_possible_call_at = self.time_provider()
        self.mutex = threading.Lock()

    def __enter__(self):
        self.mutex.acquire()
        delay = self.next_possible_call_at - self.time_provider()
        if delay > 0:
            time.sleep(delay)

    def __exit__(self, type, value, traceback):
        self.next_possible_call_at = self.time_provider() + self.time_between_calls
        self.mutex.release()

# From Enedis.SGE.GUI.0466.Guide chapeau B2B_Tiers_v1.5.0
# Le format utilisé dans les messages pour les dates est le type simple de date standard XML (xs:date)
# aaaa-mm-jj[(+|-)hh:mm]
def format_date(date):
    utc_offset = date.strftime("%z")
    if len(utc_offset) == 5 and utc_offset != "+0000":
        utc_offset = utc_offset[:3] + ':' + utc_offset[3:]
    else:
        utc_offset = ''
    return date.strftime("%Y-%m-%d") + utc_offset

# TODO make unit test
assert(format_date(dt.date(2020, 2, 5)) == "2020-02-05")

class RechercherPoint:

    WSDL = 'Enedis.SGE.GUI.0427.B2B RecherchePointV2.0_v1.1/Services/RecherchePoint/RecherchePoint-v2.0.wsdl'

    def __init__(self, session):
        self.session = session
        self.client = session.make_client(self.WSDL)

    def rechercher(self, criteres):
        try :
            with self.session.throttle:
                res = self.client.service.rechercherPoint(criteres=criteres, loginUtilisateur=self.session.login)
            # TODO read for _value_1 https://docs.python-zeep.org/en/master/datastructures.html#xsd-choice
            return {
                'code': res['header']['acquittement']['resultat']['code'],
                'message': res['header']['acquittement']['resultat']['_value_1'],
                'data': res['body']['points']['point'] if res['body']['points'] else []
            }
        except zeep.exceptions.Fault as fault:
            res = fault.detail[0][0]
            return {
                'code': res.attrib['code'],
                'message': res.text,
                'data': []
            }


class ConsultationMesures:

    WSDL = 'Enedis.SGE.GUI.0455.B2B.ConsultationMesuresV1.1_v1.1.0/Services/ConsultationMesures/ConsultationMesures-v1.1.wsdl'

    def __init__(self, session):
        self.session = session
        self.client = session.make_client(self.WSDL)

    def consulter(self, point_id, autorisation_client=1):
        try :
            with self.session.throttle:
                res = self.client.service.consulterMesures(pointId=point_id,
                                                           loginDemandeur=self.session.login,
                                                           autorisationClient=autorisation_client,
                                                           contratId=self.session.contract_id)

            return {
                'code': res['header']['acquittement']['resultat']['code'],
                'message': res['header']['acquittement']['resultat']['_value_1'],
                'data': res['body']['seriesMesuresDateesGrilleTurpe']['serie']
            }
        except zeep.exceptions.Fault as fault:
            res = fault.detail[0][0]
            return {
                'code': res.attrib['code'],
                'message': res.text,
                'data': []
            }

class ConsultationMesuresDetaillees:

    WSDL = "Enedis.SGE.GUI.0488.B2B.ConsultationMesuresDetailleesV2.0_v1.2.2/ConsultationMesuresDetaillees-v2.0.wsdl"

    def __init__(self, session):
        self.session = session
        self.client = session.make_client(self.WSDL)
        # FIXME strange http URL in wsdl
        self.client.service._binding_options["address"] = "https://sge-homologation-b2b.enedis.fr/ConsultationMesuresDetaillees/v2.0"

    def consulter(self, point_id, type_code, grandeur_physique, date_debut, date_fin, soutirage=1, injection=0, mesures_corrigees=0, accord_client=1, mesures_pas=None):

        if isinstance(date_debut, (dt.date, dt.datetime)):
            date_debut = format_date(date_debut)

        if isinstance(date_fin, (dt.date, dt.datetime)):
            date_fin = format_date(date_fin)

        try :
            demande = {
                'initiateurLogin': self.session.login,
                "pointId": point_id,
                "mesuresTypeCode": type_code,
                "grandeurPhysique": grandeur_physique,
                "soutirage": soutirage,
                "injection": injection,
                "dateDebut": date_debut,
                "dateFin": date_fin,
                "accordClient": accord_client,
                "mesuresCorrigees": mesures_corrigees
            }
            if mesures_pas is not None:
                demande['mesuresPas'] = mesures_pas
            with self.session.throttle:
                res = self.client.service.consulterMesuresDetaillees(demande=demande)

            return {
                'code': None,
                'message': None,
                'data': res
            }
        except zeep.exceptions.Fault as fault:
            res = fault.detail[0][0]
            return {
                'code': res.attrib['code'],
                'message': res.text,
                'data': {}
            }


class ConsultationDonneesTechniquesContractuelles:

    WSDL = 'Enedis.SGE.GUI.0464.B2B.ConsultationDonneesTechniquesContractuellesV1.0_V1.1.0/Services/ConsultationDonneesTechniquesContractuelles/ConsultationDonneesTechniquesContractuelles-v1.0.wsdl'

    def __init__(self, session):
        self.session = session
        self.client = session.make_client(self.WSDL)

    def consulter(self, point_id, autorisation_client=True):
        try :
            with self.session.throttle:
                res = self.client.service.consulterDonneesTechniquesContractuelles(
                    pointId=point_id,
                    loginUtilisateur=self.session.login,
                    autorisationClient=autorisation_client)

            return {
                'code': res['header']['acquittement']['resultat']['code'],
                'message': res['header']['acquittement']['resultat']['_value_1'],
                'data': res['body']['point']
            }
        except zeep.exceptions.Fault as fault:
            res = fault.detail[0][0]
            return {
                'code': res.attrib['code'],
                'message': res.text,
                'data': None
            }