# standard imports

# third-party imports

# local imports
from cic_types.schemas.load import load_validation_schema
from cic_types.validator import validate_data


kyc_json_schema = load_validation_schema(file_name='kyc.json')


class Kyc:
    """This class describes a kyc type python object that consumes kyc data and validates the data as well as provide a
    function to serialize data to a dict representation of the data.
    :cvar identification_document: The document being used for identity verification i.e [passport]
    :type identification_document: str
    :cvar identification_number: The identification number of the identification document being used for KYC.
    :type identification_number: str
    """

    identification_document: str = None
    identification_number: str = None

    def __init__(self, kyc_data: dict):
        """
        :param kyc_data:
        :type kyc_data:
        """
        self.kyc_data = kyc_data

        # attempt to validate general kyc data structure
        validate_data(instance=self.kyc_data, schema=kyc_json_schema)

        self.schema_version = 1
        self.identification_document = self.kyc_data.get("identification_document")
        self.identification_number = self.kyc_data.get("identification_number")

    def serialize(self):
        return {
            "identification_document": self.identification_document,
            "identification_number": self.identification_number
        }

