# standard imports
import enum


class MetadataPointer(enum.Enum):
    BALANCES = ':cic.balances'
    BALANCES_ADJUSTED = 'cic:balances.adjusted'
    CUSTOM = ':cic.custom'
    PERSON = ':cic.person'
    PHONE = ':cic.phone'
    PREFERENCES = ':cic.preferences'
    STATEMENT = ':cic.statement'
    TOKEN_DEFAULT = ':cic.token.default'
    TOKEN_META = ':cic.token.meta'
    TOKEN_PROOF = ':cic.token.proof'

