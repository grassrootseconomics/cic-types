# standard imports

# third-party imports
import pytest

# local imports


@pytest.fixture(scope="function")
def person_metadata():
    return {
        "date_registered": 1573505158,
        "date_of_birth": {
            "day": 13,
            "month": 6,
            "year": 1974
        },
        "gender": "male",
        "identities": {
            "evm": {
                "byzantium": {
                    "8996:bloxberg": [
                        "16ba1a17650c4001e2fa28c6f883aabe8f90d5b7",
                        "e978b4a817e95ca7f04370b83d631b8fea8e40d5"
                        ]
                }
            }
        },
        "location": {
            "area_name": "kayaba",
            "area_type": "peri-urban",
            "latitude": -13.7932245,
            "longitude": 159.183828,
        },
        "products": ["education", "transport"],
        "vcard": "QkVHSU46VkNBUkQNClZFUlNJT046My4wDQpFTUFJTDpqb25zbm93QHRoZW5vcnRoLmNvbQ0KRk46Sm9uXCwgU25vdw0KTjpTbm93O0pvbjs7Ow0KVEVMO1RZUD1DRUxMOisyNTQ3MDAwMDAwMDANCkVORDpWQ0FSRA0K"
    }


@pytest.fixture(scope="function")
def vcard_data():
    return {
        "email": "jonsnow@thenorth.com",
        "family": "Snow",
        "given": "Jon",
        "tel": "+254700000000"
    }


