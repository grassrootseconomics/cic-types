# standard imports

# third-party imports
import pytest

# local imports
from cic_types.processor import phone_number_to_e164


@pytest.mark.parametrize("phone_number, region, expected_result", [
    ("0712345678", "KE", "+254712345678"),
    ("+254787654321", "KE", "+254787654321")
])
def test_process_phone_number(expected_result, phone_number, region):
    processed_phone_number = phone_number_to_e164(phone_number=phone_number, region=region)
    assert processed_phone_number == expected_result
