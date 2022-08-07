# standard imports
import base64
import hashlib

# third-party imports
import vobject
from chainlib.chain import ChainSpec
from chainlib.eth.address import uniform, strip_0x

# local imports
from cic_types.processor import phone_number_to_e164
from cic_types.schemas.load import load_validation_schema
from cic_types.validator import validate_data

person_json_schema = load_validation_schema(file_name='person-v1.json')
vcard_json_schema = load_validation_schema(file_name='vcard-v1.json')


class Person:
    """This class describes a person type python object that takes json metadata for a user on the cic-platform.
    It serializes data to a dict representation of the data.
    :cvar date_registered: A unix timestamp representing date a user was registered in the system.
    :type date_registered: int
    :cvar year: The year of birth of the user owning an account.
    :type year: int
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

    def __init__(self):
        """
        :param person_data: A dictionary object containing all metadata for the person type.
        :type person_data: dict
        """
        self.date_registered = None
        self.user = None
        self.email = None
        self.family_name = None
        self.gender = None
        self.given_name = None
        self.identities = {}
        self.location = {}
        self.products = []
        self.tel = None
        self.date_of_birth = {}


    @classmethod
    def deserialize(cls, person_data: dict):

        p = cls()

        # TOOD: Phil, by keeping person_data in the object, you're basically doubling the memory spent to represent this object....
        p.person_data = person_data

        # attempt to validate general data format for person type
        validate_data(instance=person_data, schema=person_json_schema)

        # perform custom validations for v-object
        v_card_data = get_contact_data_from_vcard(vcard=p.person_data.get("vcard"))
        validate_data(instance=v_card_data, schema=vcard_json_schema)

        # set values
        p.schema_version = 1
        p.load_vcard(v_card_data)
        p.date_registered = p.person_data.get("date_registered")
        p.year = p.person_data.get("year")
        p.gender = p.person_data.get("gender")
        p.date_of_birth = p.person_data.get("date_of_birth")
        p.identities = p.person_data.get("identities")

        p.location = {}
        area_type = p.person_data.get("location").get("area_type")
        if area_type != None:
            p.location["area_type"] = area_type
        area_name = p.person_data.get("location").get("area_name")
        if area_name != None:
            p.location["area_name"] = area_name
        if p.person_data.get("location").get("latitude") and p.person_data.get("location").get("longitude"):
            p.location["latitude"] = p.person_data.get("location").get("latitude")
            p.location["longitude"] = p.person_data.get("location").get("longitude")

        p.products = p.person_data.get("products")

        return p


    def load_vcard(self, v_card_data):
        self.email = v_card_data.get("email")
        self.family_name = v_card_data.get("family")
        self.given_name = v_card_data.get('given')
        self.tel = v_card_data.get("tel")


    def serialize(self):
        """This function serializes a person type python object into a python dict object.
        :return: A dict representation of data as stored in cic-meta.
        :rtype: dict
        """
        serialized_metadata = {
            "date_registered": self.date_registered,
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

        if self.date_of_birth:
            serialized_metadata["date_of_birth"] = self.date_of_birth

        return serialized_metadata

    def add_identity(self, address: str, chain_spec: ChainSpec):
        address = uniform(strip_0x(address))
        manage_identity_data(blockchain_address=address,
                             chain_str=chain_spec.__str__(),
                             identity_data=self.identities)

    def __str__(self):
        return '{} {}'.format(self.given_name, self.family_name)


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


def generate_vcard_from_contact_data(family_name: str, given_name: str, region: str, tel: str, email: str = None):
    """This function generates a base64 encoded representation of a vCard object containing a user's contact data.
    :type email: str | None
    :param family_name: A user's surname formatted to read family as per vCard object conventions.
    :type family_name: str
    :param given_name: A user's given name.
    :type given_name: str
    : param region: The country code whose E164 format a phone number should be converted to.
    : param region: str
    :param tel: An E164 formatted phone number associated with a user's account.
    :type tel: str
    :return: A base64 encoded representation of a vcard object.
    :rtype: str
    """

    # process phone number
    tel = phone_number_to_e164(phone_number=tel, region=region)
    v_card = vobject.vCard()
    if email:
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


def identity_tag(chain_spec_dict: dict) -> str:
    """ This function parses the chain spec dict and checks for the presence of the optional common name and returns the
    appropriate identity tag.
    :param chain_spec_dict: A dictionary representation of the chain spec object.
    :type chain_spec_dict: dict
    :return: Colon separated string of the format network_id | network_id:common_name as per common name presence.
    :rtype: str
    """
    network_id = chain_spec_dict.get('network_id')
    common_name = chain_spec_dict.get('common_name')
    return f'{network_id}:{common_name}' if common_name else f'{network_id}'


def manage_identity_data(blockchain_address: str, chain_str: str, identity_data: dict = None):
    """This function implements a management strategy for the identities held in metadata for an account, it creates
    a dictionary object that stores the network and child network id against a list of addresses associated with an
    account.
    :param blockchain_address: An address on a wallet.
    :type blockchain_address: str
    :param chain_str: The chain name and network id.
    :type chain_str: str
    :param identity_data: A dictionary object containing data on the identities.
    :type identity_data: dict
    :return: A new or edited version of the identity data dictionary object.
    :rtype: dict
    """
    addresses = []
    chain_spec = ChainSpec.from_chain_str(chain_str).asdict()
    arch = chain_spec.get('arch')
    fork = chain_spec.get('fork')
    common_name = chain_spec.get("common_name")
    network_id = chain_spec.get("network_id")
    identities = f'{network_id}:{common_name}' if common_name else f'{network_id}'

    if not identity_data:
        identity_data = {
            arch: {
                fork: {
                    identities: addresses + [blockchain_address]
                }
            }
        }
    else:
        if identity_data.get(arch):
            addresses = identity_data[arch][fork][identities]

        identity_data[arch] = {
            fork: {
                identities: addresses + [blockchain_address]
            }
        }

    return identity_data
