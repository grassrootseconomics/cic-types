# standard imports

# third-party imports

# local imports
from cic_types.models.person import (
    Person,
    get_contact_data_from_vcard,
    generate_metadata_pointer,
    generate_vcard_from_contact_data
)


def test_person(sample_person_metadata):
    # check that all validation pass
    person = Person(person_data=sample_person_metadata)

    assert person.date_registered == sample_person_metadata.get("date_registered")
    assert person.gender == sample_person_metadata.get("gender")
    assert person.key == sample_person_metadata.get("key")
    assert person.latitude == sample_person_metadata.get("location").get("latitude")
    assert person.longitude == sample_person_metadata.get("location").get("longitude")
    assert sample_person_metadata.get("location").get("external") == {}
    assert person.selling == sample_person_metadata.get("selling")

    v_card_data = get_contact_data_from_vcard(vcard=sample_person_metadata.get("vcard"))
    assert person.email == v_card_data.get("email")
    assert person.family_name == v_card_data.get("family")
    assert person.given_name == v_card_data.get("given")
    assert person.tel == v_card_data.get("tel")


def test_get_contact_data_from_vcard(sample_person_metadata):
    v_card_data = get_contact_data_from_vcard(vcard=sample_person_metadata.get("vcard"))
    assert v_card_data.get("email") == "jonsnow@thenorth.com"
    assert v_card_data.get("family") == "Snow"
    assert v_card_data.get("given") == "Jon"
    assert v_card_data.get("tel") == "+254700000000"


def test_generate_metadata_pointer(sample_person_metadata):
    blockchain_address = sample_person_metadata.get("key").get("ethereum")[0]
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
