# standard imports
import json
import logging
import os
from typing import Dict, Union

from cic_types.condiments import MetadataPointer
from cic_types.ext.requests import error_handler, make_request
from cic_types.processor import generate_metadata_pointer

# local imports
from .signer import Signer

# external imports


logg = logging.getLogger(__file__)


class Metadata:
    """
    :cvar base_url: The base url or the metadata server.
    :type base_url: str
    :cvar auth_token: The auth token for the metadata server. 
    :type auth_token: str
    """

    base_url = None
    auth_token = None


class MetadataRequestsHandler(Metadata):

    def __init__(self, cic_type: MetadataPointer, identifier: bytes, engine: str = 'pgp'):
        """"""
        self.cic_type = cic_type
        self.engine = engine
        self.headers = {
            'X-CIC-AUTOMERGE': 'server',
            'Content-Type': 'application/json',
            'Authorization': f'Basic {self.auth_token}'
        }
        self.identifier = identifier
        if cic_type == MetadataPointer.NONE:
            self.metadata_pointer = identifier.hex()
        else:
            self.metadata_pointer = generate_metadata_pointer(
                identifier=self.identifier,
                cic_type=self.cic_type
            )
        if self.base_url:
            self.url = os.path.join(self.base_url, self.metadata_pointer)

    def create(self, data: Union[Dict, str]):
        """"""
        data = json.dumps(data).encode('utf-8')
        result = make_request(method='POST', url=self.url, data=data, headers=self.headers)

        error_handler(result=result)
        metadata = result.json()
        return self.edit(data=metadata)

    def edit(self, data: Union[Dict, str]):
        """"""
        cic_meta_signer = Signer()
        signature = cic_meta_signer.sign_digest(data=data)
        algorithm = cic_meta_signer.get_operational_key().get('algo')
        formatted_data = {
            'm': json.dumps(data),
            's': {
                'engine': self.engine,
                'algo': algorithm,
                'data': signature,
                'digest': data.get('digest'),
            }
        }
        formatted_data = json.dumps(formatted_data)
        result = make_request(method='PUT', url=self.url, data=formatted_data, headers=self.headers)
        logg.info(f'signed metadata submission status: {result.status_code}.')
        error_handler(result=result)
        try:
            decoded_identifier = self.identifier.decode("utf-8")
        except UnicodeDecodeError:
            decoded_identifier = self.identifier.hex()
        return result

    def query(self):
        """"""
        result = make_request(method='GET', url=self.url)
        error_handler(result=result)
        result_data = result.json()
        if not isinstance(result_data, dict):
            raise ValueError(f'invalid result data object: {result_data}.')
        return result
