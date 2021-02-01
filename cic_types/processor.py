# standard imports

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
