# standard imports

# third-party imports
import pytest
from jsonschema.exceptions import ValidationError

# local imports
from cic_types.schemas.person import person_json_schema, vcard_json_schema
from cic_types.validator import validate_data


def test_invalid_data(sample_vcard_data):
    with pytest.raises(ValidationError) as error:
        sample_vcard_data['tel'] = 123456789
        validate_data(instance=sample_vcard_data, schema=vcard_json_schema)
    assert str(error.value) == "123456789 is not of type 'string'\n\nFailed validating 'type' in schema['properties']['tel']:\n    {'pattern': '^([+254]?[0-9]{12})$', 'type': 'string'}\n\nOn instance['tel']:\n    123456789"
