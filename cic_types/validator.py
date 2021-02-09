# standard imports
import re

# third-party imports
from jsonschema import Draft7Validator

# local imports


def validate_data(instance: dict, schema: dict):
    """This function user the draft7 validator to check a python dict object against pre-defined validation criteria
    described in json schemas.
    :param instance: The instance of the dict to be validated.
    :type instance: dict
    :param schema: The schema object defining the criteria to verify a dict object's structure and data.
    :type schema: dict
    :return: A boolean value representing validity of the data object being validated.
    :rtype: bool
    """
    validator = Draft7Validator(schema=schema)
    return validator.validate(instance)
