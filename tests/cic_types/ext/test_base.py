# standard imports
import json
import os

# external imports
import requests_mock

# local imports
from cic_types.condiments import MetadataPointer
from cic_types.ext.metadata import MetadataRequestsHandler
from cic_types.processor import generate_metadata_pointer

# external imports


def test_metadata_requests_handler(load_config,
                                   person_metadata,
                                   setup_metadata_request_handler,
                                   setup_metadata_signer):
    identifier = bytes.fromhex(person_metadata['identities']['evm']['bloxberg:8996'][0])
    cic_type = MetadataPointer.PERSON
    metadata_client = MetadataRequestsHandler(cic_type, identifier)
    assert metadata_client.cic_type == cic_type
    assert metadata_client.engine == 'pgp'
    assert metadata_client.identifier == identifier
    assert metadata_client.metadata_pointer == generate_metadata_pointer(identifier, cic_type)
    assert metadata_client.url == os.path.join(load_config.get('CIC_META_URL'), metadata_client.metadata_pointer)

    with requests_mock.Mocker(real_http=False) as request_mocker:
        request_mocker.register_uri('POST', metadata_client.url, status_code=200, reason='OK', json=person_metadata)
        person_metadata['digest'] = os.urandom(20).hex()
        request_mocker.register_uri('PUT', metadata_client.url, status_code=200, reason='OK', json=person_metadata)
        result = metadata_client.create(person_metadata)
        assert result.json() == person_metadata
        assert result.status_code == 200
        person_metadata.pop('digest')
        request_mocker.register_uri('GET', metadata_client.url, status_code=200, reason='OK', json=person_metadata)
        result = metadata_client.query()
        assert result.json() == person_metadata
