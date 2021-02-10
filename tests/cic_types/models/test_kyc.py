# standard imports
import json

# third-party imports

# local imports
from cic_types.models.kyc import Kyc


def test_kyc(sample_kyc_metadata):
    kyc = Kyc(kyc_data=sample_kyc_metadata)

    assert kyc.identification_document == sample_kyc_metadata.get("identification_document")
    assert kyc.identification_number == sample_kyc_metadata.get("identification_number")

    kyc_data_serialized = kyc.serialize()
    assert kyc_data_serialized.get("identification_document") == sample_kyc_metadata.get("identification_document")
    assert kyc_data_serialized.get("identification_number") == sample_kyc_metadata.get("identification_number")

