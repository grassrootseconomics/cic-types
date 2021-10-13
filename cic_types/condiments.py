# standard imports
import enum


class MetadataPointer(enum.Enum):
    ADJUSTED_BALANCE = ':cic.adjusted_balance'
    BALANCES = ':cic.balances'
    CUSTOM = ':cic.custom'
    DEFAULT_TOKEN = ':cic.default_token_data'
    PERSON = ':cic.person'
    PHONE = ':cic.phone'
    PREFERENCES = ':cic.preferences'
    STATEMENT = ':cic.statement'
    TOKEN = ':cic.token'

