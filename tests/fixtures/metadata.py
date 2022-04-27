# standard imports
import logging
import os
import tempfile

# external imports
import pytest

# local imports
from cic_types.ext.metadata.signer import Signer
from cic_types.ext.metadata import Metadata


logg = logging.getLogger(__file__)


@pytest.fixture(scope='function')
def setup_metadata_signer(load_config):
    temp_dir = tempfile.mkdtemp(dir='/tmp')
    logg.debug(f'Created temp dir: {temp_dir}')
    Signer.gpg_path = temp_dir
    Signer.gpg_passphrase = load_config.get('PGP_PASSPHRASE')
    Signer.key_file_path = os.path.join(load_config.get('PGP_KEYS_PATH'), load_config.get('PGP_PRIVATE_KEYS'))


@pytest.fixture(scope='function')
def setup_metadata_request_handler(load_config):
    Metadata.base_url = load_config.get('CIC_META_URL')
