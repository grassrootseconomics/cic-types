# standard imports

# third-party imports
import pytest
from jsonschema.exceptions import ValidationError

# local imports
from cic_types.models.person import vcard_json_schema
from cic_types.validator import validate_data


def test_invalid_data(vcard_data):
    with pytest.raises(ValidationError) as error:
        vcard_data['tel'] = 123456789
        validate_data(instance=vcard_data, schema=vcard_json_schema)
    assert str(error.value) == "123456789 is not of type 'string'\n\nFailed validating 'type' in schema['properties']['tel']:\n    {'pattern': '^(\\\\+?[0-9]+)$', 'type': 'string'}\n\nOn instance['tel']:\n    123456789"
