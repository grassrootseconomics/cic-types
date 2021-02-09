# standard imports
import base64
import hashlib
import json

# third-party imports
import vobject

# local imports
from cic_types.processor import phone_number_to_e164
from cic_types.schemas.load import load_validation_schema
from cic_types.validator import validate_data

person_json_schema = load_validation_schema(file_name='person.json')
vcard_json_schema = load_validation_schema(file_name='vcard.json')


class Person:
    """This class describes a person type python object that take json metadata for a user on the cic-platform.
    It serializes data to json for interfacing with none-python systems and innately offers a python object that can be
    used on systems running python code.
    :cvar date_registered: A unix timestamp representing date a user was registered in the system.
    :type date_registered: int
    :cvar age: The age of the user owning an account.
    :type age: int
    :cvar email: An email address associated with an user's account.
    :type email: str
    :cvar family_name: A user's surname formatted to read family as per vCard object conventions.
    :type family_name: str
    :cvar gender: A user's gender.
    :type gender: str
    :cvar given_name: A user's given name.
    :type given_name: str
    :cvar identities: An object containing identity data for accounts on the system.
    :type identities: dict
    :cvar location: A dictionary containing location data.
    :type location: dict
    :cvar products: A list object representing businesses or services a user may offer and trade in on the system.
    :type products: list
    :cvar tel: An E164 formatted phone number associated with a user's account.
    :type tel: str
    :raises ValidationError: if any value contravenes set validation parameters in the described json schemas.
    """
    date_registered: int = None
    age: int = None
    email: str = None
    family_name: str = None
    gender: str = None
    given_name: str = None
    identities: dict = None
    location: dict = None
    products: list = None
    tel: str = None

    def __init__(self, person_data: dict):
        """
        :param person_data: A dictionary object containing all metadata for the person type.
        :type person_data: dict
        """
        self.person_data = person_data

        # attempt to validate general data format for person type
        validate_data(instance=person_data, schema=person_json_schema)

        # perform custom validations for v-object
        v_card_data = get_contact_data_from_vcard(vcard=self.person_data.get("vcard"))
        validate_data(instance=v_card_data, schema=vcard_json_schema)

        # set values
        self.schema_version = 1
        self.date_registered = self.person_data.get("date_registered")
        self.age = self.person_data.get("age")
        self.email = v_card_data.get("email")
        self.family_name = v_card_data.get("family")
        self.gender = self.person_data.get("gender")
        self.given_name = v_card_data.get('given')
        self.identities = person_data.get("identities")
        self.location = {
            "area_name": self.person_data.get("location").get("area_name"),
            "area_type": self.person_data.get("location").get("area_type"),
            "latitude": self.person_data.get("location").get("latitude"),
            "longitude": self.person_data.get("location").get("longitude")
        }
        self.products = self.person_data.get("products")
        self.tel = v_card_data.get("tel")

    def serialize(self):
        """This function serializes a person type python object into a JSON formatted string.
        :return: A JSON representation of data as stored in cic-meta.
        :rtype: str
        """
        person_data = {
            "date_registered": self.date_registered,
            "age": self.age,
            "gender": self.gender,
            "identities": self.identities,
            "location": self.location,
            "products": self.products,
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
    :return: A sha256 hash of an identifier and cic-type.
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


def manage_identity_data(blockchain_address: str, chain_spec: str, blockchain_type: str, identity_data: dict = None):
    """This function implements a management strategy for the identities held in metadata for an account, it creates
    a dictionary object that stores the network and child network id against a list of addresses associated with an
    account.
    :param blockchain_address: An address on a wallet.
    :type blockchain_address: str
    :param chain_spec: The chain name and network id.
    :type chain_spec: str
    :param blockchain_type: The blockchain network on which the account exists.
    :type blockchain_type: str
    :param identity_data: A dictionary object containing data on the identities.
    :type identity_data: dict
    :return: A new or edited version of the identity data dictionary object.
    :rtype: dict
    """
    addresses = []
    if not identity_data:
        identity_data = {
            blockchain_type: {
                chain_spec: addresses + [blockchain_address]
            }
        }
        return identity_data
    else:
        if identity_data.get(blockchain_type):
            addresses = identity_data.get(blockchain_type).get(chain_spec) or []

        identity_data[blockchain_type] = {
            chain_spec: addresses + [blockchain_address]
        }
        return identity_data
