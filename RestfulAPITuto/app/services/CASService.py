import xml.etree.ElementTree as ET

import requests

from app.config import Config


class CASService:
    root: ET.ElementTree

    #  take note about the memory allocation, multi user condition might return same value for all user?
    @staticmethod
    def get_cas_respond(service, ticket):
        url = Config.CAS_URL + "/cas/p3/serviceValidate"
        # defining a params dict for the parameters to be sent to the API
        params = {'service': service, 'ticket': ticket}
        # sending get request and saving the response as response object
        r = requests.get(url=url, params=params)
        # extracting data in json format
        data_string = r.text
        CASService.root = ET.ElementTree(ET.fromstring(data_string))
        return CASService.root

    @staticmethod
    def get_root():
        return CASService.root
