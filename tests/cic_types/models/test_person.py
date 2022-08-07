# standard imports
import os
import json

# third-party imports
from chainlib.chain import ChainSpec
from chainlib.eth.address import to_checksum

# local imports
from cic_types.models.person import (
    Person,
    get_contact_data_from_vcard,
    generate_vcard_from_contact_data,
    manage_identity_data
)


def test_person(person_metadata):
    # check that all validation pass
    person = Person.deserialize(person_data=person_metadata)

    assert person.date_registered == person_metadata.get("date_registered")
    assert person.date_of_birth == person_metadata.get("date_of_birth")
    assert person.gender == person_metadata.get("gender")
    assert person.identities == person_metadata.get("identities")
    assert person.location == person_metadata.get("location")
    assert person.products == person_metadata.get("products")

    v_card_data = get_contact_data_from_vcard(vcard=person_metadata.get("vcard"))
    assert person.email == v_card_data.get("email")
    assert person.family_name == v_card_data.get("family")
    assert person.given_name == v_card_data.get("given")
    assert person.tel == v_card_data.get("tel")

    person_serialized = person.serialize(region='KE')

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
        tel=vcard_data.get("tel"),
        region='KE'
    )
    assert person_metadata.get("vcard") == v_card


def test_manage_identity_data(person_metadata):
    blockchain_address = "16ba1a17650c4001e2fa28c6f883jdhud458df654d"
    chain_str = "evm:byzantium:8996:bloxberg"
    chain_spec = ChainSpec.from_chain_str(chain_str).asdict()
    arch = chain_spec.get('arch')
    fork = chain_spec.get('fork')
    network_id_common_name = f'{chain_spec.get("network_id")}:{chain_spec.get("common_name")}'
    identities = person_metadata.get("identities")

    identity_data = manage_identity_data(
        blockchain_address=blockchain_address,
        chain_str=chain_str,
        identity_data=identities
    )

    assert len(identity_data.get(arch).get(fork).get(network_id_common_name)) == 3
    alternative_identity_data = {}
    assert bool(alternative_identity_data) is False
    alternative_identity_data = manage_identity_data(
        blockchain_address=blockchain_address,
        chain_str=chain_str,
    )
    assert len(alternative_identity_data.get(arch).get(fork).get(network_id_common_name)) == 1


def test_chain_spec_set(person_metadata):
    p = Person.deserialize(person_metadata)
    chain_spec = ChainSpec('foo', 'bar', 42)
    address = os.urandom(20).hex()
    p.add_identity(address, chain_spec)
    assert p.identities['foo']['bar']['42'][0] == address
