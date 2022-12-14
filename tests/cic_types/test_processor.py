# standard imports

# third-party imports
import pytest

# local imports
from cic_types.processor import phone_number_to_e164, generate_metadata_pointer
from cic_types.condiments import MetadataPointer


@pytest.mark.parametrize("phone_number, region, expected_result", [
    ("0712345678", "KE", "+254712345678"),
    ("+254787654321", "KE", "+254787654321")
])
def test_process_phone_number(expected_result, phone_number, region):
    processed_phone_number = phone_number_to_e164(phone_number=phone_number, region=region)
    assert processed_phone_number == expected_result


def test_generate_metadata_pointer(person_metadata):
    blockchain_address = person_metadata.get("identities").get("evm").get('byzantium').get("8996:bloxberg")[0]
    identifier = bytes.fromhex(blockchain_address)
    metadata_pointer = generate_metadata_pointer(identifier=identifier, cic_type=MetadataPointer.PERSON)
    assert len(metadata_pointer) == 64
