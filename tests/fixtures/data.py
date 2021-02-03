# standard imports

# third-party imports
import pytest

# local imports


@pytest.fixture(scope="function")
def sample_person_metadata():
    return {
        "date_registered": 1573505158,
        "vcard": "QkVHSU46VkNBUkQNClZFUlNJT046My4wDQpFTUFJTDpqb25zbm93QHRoZW5vcnRoLmNvbQ0KRk46Sm9uXCwgU25vdw0KTjpTbm93O0pvbjs7Ow0KVEVMO1RZUD1DRUxMOisyNTQ3MDAwMDAwMDANCkVORDpWQ0FSRA0K",
        "gender": "male",
        "key": {
            "ethereum": [
                "0x16ba1a17650c4001e2fa28c6f883aabe8f90d5b7",
                "0xE978b4A817e95Ca7F04370B83d631b8fea8E40D5"
            ]
        },
        "location": {
            "latitude": "-13.7932245",
            "longitude": "159.183828",
            "external": {}
        },
        "selling": [
            "education",
            "transport"
        ]
    }


@pytest.fixture(scope="function")
def sample_vcard_data():
    return {
        "email": "jonsnow@thenorth.com",
        "family": "Snow",
        "given": "Jon",
        "tel": "+254700000000"
    }