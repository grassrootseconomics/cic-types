# standard imports
import hashlib

# third-party imports
import phonenumbers

# local imports


def phone_number_to_e164(phone_number: str, region: str):
    """This function parses any phone number for the provided region
    :param phone_number: A string with a phone number.
    :type phone_number: str
    :param region: Caller defined region
    :type region: str
    :return: The parsed phone number value based on the defined region
    :rtype: str
    """
    if not isinstance(phone_number, str):
        try:
            phone_number = str(int(phone_number))

        except ValueError:
            pass

    phone_number_object = phonenumbers.parse(phone_number, region)
    processed_phone_number = phonenumbers.format_number(phone_number_object, phonenumbers.PhoneNumberFormat.E164)

    return processed_phone_number


def generate_metadata_pointer(identifier: bytes, cic_type: str):
    """This function generates a pointer to access data for a specific user's account in cic-meta. It hashes the
    identifier against a string representing a cic-type and creates an index value that can be used to look up account
    metadata.
    :param identifier: A unique identifier that can be used to look up an account's metadata e.g a blockchain address or
    phone number.
    :type identifier: bytes
    :param cic_type: type descriptor for cic specific objects.
    :type cic_type: str
    :return: A sha256 hash of an identifier and cic-type.
    :rtype: str
    """
    hash_object = hashlib.new("sha256")
    hash_object.update(identifier)
    hash_object.update(cic_type.encode(encoding="utf-8"))
    return hash_object.digest().hex()
