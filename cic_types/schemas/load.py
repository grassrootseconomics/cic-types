# standard-imports
import json
import logging
import os

# third-party imports

# local imports

logging.basicConfig()
logg = logging.getLogger()

parent_dir = os.path.dirname(os.path.dirname(__file__))


def load_validation_schema(file_name: str):
    """This function takes a file name of a validation schema, it then reads the successive file and returns a dict of
    the corresponding elements in the schema
        :param file_name: The name of the JSON file containing data.
        :type file_name: str
        :return: A validation schema for a specific set of data.
        :rtype: dict
        """
    filepath = os.path.join(parent_dir, f'schemas/{file_name}')
    data_file = open(filepath)
    json_data = json.load(data_file)
    logg.debug(f'Loading data from: {filepath}')
    data_file.close()

    return json_data
