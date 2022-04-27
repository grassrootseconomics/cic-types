# standard imports
import json
import os

# third-party imports
from chainlib.chain import ChainSpec
from chainlib.eth.address import to_checksum
# local imports
from cic_types.models.tx import TokenTx


def test_tx(tx_dict):
    # check that all validation pass
    tx = TokenTx.from_dict(tx_dict)
    assert tx.block_number == tx_dict["block_number"]
    assert tx.tx_index == tx_dict["tx_index"]
    assert tx.tx_hash == tx_dict["tx_hash"]
    assert tx.date_block == tx_dict["date_block"]
    assert tx.sender == to_checksum(tx_dict["sender"])
    assert tx.recipient == to_checksum(tx_dict["recipient"])
    assert tx.from_value == tx_dict["from_value"]
    assert tx.to_value == tx_dict["to_value"]
    assert tx.source_token == to_checksum(tx_dict["source_token"])
    assert tx.destination_token == to_checksum(tx_dict["destination_token"])
    assert tx.success == tx_dict["success"]
    assert tx.tx_type == tx_dict["tx_type"]
