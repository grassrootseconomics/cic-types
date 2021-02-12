# standard imports
import json

# third-party imports

# local imports
from cic_types.models.person import (
    Person,
    get_contact_data_from_vcard,
    generate_metadata_pointer,
    generate_vcard_from_contact_data,
    manage_identity_data
)


def test_person(sample_person_metadata):
    # check that all validation pass
    person = Person(person_data=sample_person_metadata)

    assert person.date_registered == sample_person_metadata.get("date_registered")
    assert person.age == sample_person_metadata.get("age")
    assert person.gender == sample_person_metadata.get("gender")
    assert person.identities == sample_person_metadata.get("identities")
    assert person.location == sample_person_metadata.get("location")
    assert person.products == sample_person_metadata.get("products")

    v_card_data = get_contact_data_from_vcard(vcard=sample_person_metadata.get("vcard"))
    assert person.email == v_card_data.get("email")
    assert person.family_name == v_card_data.get("family")
    assert person.given_name == v_card_data.get("given")
    assert person.tel == v_card_data.get("tel")

    person_serialized = json.loads(person.serialize())

    assert person_serialized.get("date_registered") == sample_person_metadata.get("date_registered")
    assert person_serialized.get("gender") == sample_person_metadata.get("gender")
    assert person_serialized.get("identities") == sample_person_metadata.get("identities")
    assert person_serialized.get("location") == sample_person_metadata.get("location")
    assert person_serialized.get("products") == sample_person_metadata.get("products")


def test_get_contact_data_from_vcard(sample_person_metadata):
    v_card_data = get_contact_data_from_vcard(vcard=sample_person_metadata.get("vcard"))
    assert v_card_data.get("email") == "jonsnow@thenorth.com"
    assert v_card_data.get("family") == "Snow"
    assert v_card_data.get("given") == "Jon"
    assert v_card_data.get("tel") == "+254700000000"


def test_generate_metadata_pointer(sample_person_metadata):
    blockchain_address = sample_person_metadata.get("identities").get("evm").get("Bloxberg:8995")[0]
    identifier = bytes.fromhex(blockchain_address[2:])
    metadata_pointer = generate_metadata_pointer(identifier=identifier, cic_type='cic.type')
    assert len(metadata_pointer) == 64


def test_generate_vcard_from_contact_data(sample_person_metadata, sample_vcard_data):
    v_card = generate_vcard_from_contact_data(
        email=sample_vcard_data.get("email"),
        family_name=sample_vcard_data.get("family"),
        given_name=sample_vcard_data.get("given"),
        tel=sample_vcard_data.get("tel")
    )
    assert sample_person_metadata.get("vcard") == v_card


def test_manage_identity_data(sample_person_metadata):
    blockchain_address = "0x16ba1a17650c4001e2fa28c6f883jdhud458df654d"
    chain_spec = "Bloxberg:8995"
    blockchain_type = "evm"
    identities = sample_person_metadata.get("identities")

    identity_data = manage_identity_data(
        blockchain_address=blockchain_address,
        chain_spec=chain_spec,
        blockchain_type=blockchain_type,
        identity_data=identities
    )
    assert len(identity_data.get(blockchain_type).get(chain_spec)) == 3
    alternative_identity_data = {}
    assert bool(alternative_identity_data) is False
    alternative_identity_data = manage_identity_data(
        blockchain_address=blockchain_address,
        chain_spec=chain_spec,
        blockchain_type=blockchain_type
    )
    assert len(alternative_identity_data.get(blockchain_type).get(chain_spec)) == 1

