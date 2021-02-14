# standard imports
import json

# third-party imports

# local imports
from cic_types.models.person import (
    Person,
    get_contact_data_from_vcard,
    generate_vcard_from_contact_data,
    manage_identity_data
)


def test_person(person_metadata):
    # check that all validation pass
    person = Person(person_data=person_metadata)

    assert person.date_registered == person_metadata.get("date_registered")
    assert person.year == person_metadata.get("year")
    assert person.gender == person_metadata.get("gender")
    assert person.identities == person_metadata.get("identities")
    assert person.location == person_metadata.get("location")
    assert person.products == person_metadata.get("products")

    v_card_data = get_contact_data_from_vcard(vcard=person_metadata.get("vcard"))
    assert person.email == v_card_data.get("email")
    assert person.family_name == v_card_data.get("family")
    assert person.given_name == v_card_data.get("given")
    assert person.tel == v_card_data.get("tel")

    person_serialized = person.serialize()

    assert person_serialized.get("date_registered") == person_metadata.get("date_registered")
    assert person_serialized.get("gender") == person_metadata.get("gender")
    assert person_serialized.get("identities") == person_metadata.get("identities")
    assert person_serialized.get("location") == person_metadata.get("location")
    assert person_serialized.get("products") == person_metadata.get("products")


def test_get_contact_data_from_vcard(person_metadata):
    v_card_data = get_contact_data_from_vcard(vcard=person_metadata.get("vcard"))
    assert v_card_data.get("email") == "jonsnow@thenorth.com"
    assert v_card_data.get("family") == "Snow"
    assert v_card_data.get("given") == "Jon"
    assert v_card_data.get("tel") == "+254700000000"


def test_generate_vcard_from_contact_data(person_metadata, vcard_data):
    v_card = generate_vcard_from_contact_data(
        email=vcard_data.get("email"),
        family_name=vcard_data.get("family"),
        given_name=vcard_data.get("given"),
        tel=vcard_data.get("tel")
    )
    assert person_metadata.get("vcard") == v_card


def test_manage_identity_data(person_metadata):
    blockchain_address = "0x16ba1a17650c4001e2fa28c6f883jdhud458df654d"
    chain_spec = "Bloxberg:8995"
    blockchain_type = "evm"
    identities = person_metadata.get("identities")

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

