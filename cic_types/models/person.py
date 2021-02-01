# standard imports
import base64
import hashlib
import json

# third-party imports
import vobject

# local imports
from cic_types.processor import phone_number_to_e164
from cic_types.schemas.person import person_json_schema, vcard_json_schema
from cic_types.validator import validate_data


class Person:
    """This class describes a person type python object that take json metadata for a user on the cic-platform.
    It serializes data to json for interfacing with none-python systems and innately offers a python object that can be
    used on systems running python code.
    :cvar date_registered: A unix timestamp representing date a user was registered in the system.
    :type date_registered: int
    :cvar email: An email address associated with an user's account.
    :type email: str
    :cvar family_name: A user's surname formatted to read family as per vCard object conventions.
    :type family_name: str
    :cvar gender: A user's gender.
    :type gender: str
    :cvar given_name: A user's given name.
    :type given_name: str
    :cvar key: A list object containing key value pairs of tokens and addresses for users on the system.
    :type key: list
    :cvar latitude: Co-ordinate representing user's residence in latitude.
    :type latitude: str
    :cvar longitude: Co-ordinate representing user's residence in longitude.
    :type longitude: str
    :cvar selling: A list object representing businesses or services a user may offer and trade in on the system.
    :type selling: list
    :cvar tel: An E164 formatted phone number associated with a user's account.
    :type tel: str
    :raises ValidationError: if any value contravenes set validation parameters in the described json schemas.
    """
    date_registered: int = None
    email: str = None
    family_name: str = None
    gender: str = None
    given_name: str = None
    key: dict = None
    latitude: float = None
    longitude: float = None
    selling: list = None
    tel: str = None

    def __init__(self, person_data: dict):
        """
        :param person_data:
        :type person_data:
        """
        self.person_data = person_data

        # attempt to validate general data format for person type
        validate_data(instance=person_data, schema=person_json_schema)

        # perform custom validations for v-object
        v_card_data = get_contact_data_from_vcard(vcard=self.person_data.get("vcard"))
        validate_data(instance=v_card_data, schema=vcard_json_schema)

        # set values
        self.date_registered = self.person_data.get("date_registered")
        self.email = v_card_data.get("email")
        self.family_name = v_card_data.get("family")
        self.gender = self.person_data.get("gender")
        self.given_name = v_card_data.get('given')
        self.key = self.person_data.get("key")
        self.latitude = self.person_data.get("location").get("latitude")
        self.longitude = self.person_data.get("location").get("longitude")
        self.selling = self.person_data.get("selling")
        self.tel = v_card_data.get("tel")

    def serialize(self):
        """This function serializes a person type python object into a JSON formatted string.
        :return: A JSON representation of data as stored in cic-meta.
        :rtype: str
        """
        person_data = {
            "date_registered": self.date_registered,
            "gender": self.gender,
            "key": self.key,
            "location": {
                "latitude": self.latitude,
                "longitude": self.longitude,
                "external": {}
            },
            "selling": self.selling,
            "vcard": generate_vcard_from_contact_data(
                email=self.email,
                family_name=self.family_name,
                given_name=self.given_name,
                tel=self.tel
            )
        }
        return json.dumps(person_data)


def generate_metadata_pointer(identifier: bytes, cic_type: str):
    """This function generates a pointer to access data for a specific user's account in cic-meta. It hashes the
    identifier against a string representing a cic-type and creates an index value that can be used to look up account
    metadata.
    :param identifier: A unique identifier that can be used to look up an account's metadata e.g a blockchain address or
    phone number.
    :type identifier: bytes
    :param cic_type: type descriptor for cic specific objects.
    :type cic_type: str
    :return: A sha256 hash of a blockchain address and cic-type.
    :rtype: str
    """
    hash_object = hashlib.new("sha256")
    hash_object.update(identifier)
    hash_object.update(cic_type.encode(encoding="utf-8"))
    return hash_object.digest().hex()


# TODO: Figure out a clean way to handle entries in the vcard object with multiple values.
def get_contact_data_from_vcard(vcard: str):
    """This function parses a vcard object and builds a python dictionary containing the vcard's constituent information.
    :param vcard: A base64 encoded representation of a vcard object.
    :type vcard: str
    :return: A dictionary of a user's contact information.
    :rtype: dict
    """
    contact_data = {}
    v_card_serialized = base64.b64decode(vcard.encode("utf-8"))
    v_card_object = vobject.readOne(stream=v_card_serialized.decode("utf-8"), validate=True)
    for key, data in v_card_object.contents.items():
        # parse name object
        if key == "n":
            contact_data["given"] = data[0].value.given
            contact_data["family"] = data[0].value.family
        contact_data[key] = data[0].value
        # clean v-object
        v_object_values = contact_data.keys()
        if "n" in v_object_values:
            contact_data.pop("n")
        elif "fn" in v_object_values:
            contact_data.pop("fn")
        elif "version" in v_object_values:
            contact_data.pop("version")
    return contact_data


def generate_vcard_from_contact_data(email: str, family_name: str, given_name: str, tel: str):
    """This function generates a base64 encoded representation of a vCard object containing a user's contact data.
    :type email: str
    :param family_name: A user's surname formatted to read family as per vCard object conventions.
    :type family_name: str
    :param given_name: A user's given name.
    :type given_name: str
    :param tel: An E164 formatted phone number associated with a user's account.
    :type tel: str
    :return: A base64 encoded representation of a vcard object.
    :rtype: str
    """

    # process phone number
    tel = phone_number_to_e164(phone_number=tel, region="KE")

    v_card = vobject.vCard()
    v_card.add("email")
    v_card.email.value = email
    v_card.add("n")
    v_card.n.value = vobject.vcard.Name(given=given_name, family=family_name)
    v_card.add("fn")
    v_card.fn.value = f"{given_name}, {family_name}"
    v_card.add("tel")
    v_card.tel.typ_param = "CELL"
    v_card.tel.value = tel

    v_card_serialized = v_card.serialize()
    v_card_base64 = base64.b64encode(v_card_serialized.encode(encoding="utf-8"))
    return v_card_base64.decode(encoding="utf-8")
