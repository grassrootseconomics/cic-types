# standard imports
import logging
import os

# external imports
import pytest
from confini import Config

# local imports


fixtures_dir = os.path.dirname(__file__)
root_directory = os.path.dirname(os.path.dirname(fixtures_dir))

logg = logging.getLogger(__name__)


@pytest.fixture(scope='session')
def load_config():
    config_directory = os.path.join(root_directory, 'config/test')
    config = Config(default_dir=config_directory)
    config.process()
    logg.debug('config loaded\n{}'.format(config))
    return config
