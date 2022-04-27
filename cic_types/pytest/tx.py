import pytest


@pytest.fixture(scope="function")
def tx_dict():
    return {
        "block_number": 4774,
        "tx_index": 3,
        "tx_hash": "f7524b9ffad487d7b5ee80f71f894d6e9570e63894dbaa13409232be79b95e91",
        "date_block": 1650435900.0,
        "sender": "289DeFD53E2D96F05Ba29EbBebD9806C94d04Cb6",
        "recipient": "289DeFD53E2D96F05Ba29EbBebD9806C94d04Cb6",
        "from_value": 0,
        "to_value": 0,
        "source_token": "aB89822F31c2092861F713F6F34bd6877a8C1878",
        "destination_token": "aB89822F31c2092861F713F6F34bd6877a8C1878",
        "success": True,
        "tx_type": "erc20.transfer"
    }
