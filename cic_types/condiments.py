# standard imports
import enum


class MetadataPointer(enum.Enum):
    NONE = None
    BALANCES = ':cic.balances'
    BALANCES_ADJUSTED = 'cic:balances.adjusted'
    CUSTOM = ':cic.custom'
    PERSON = ':cic.person'
    PHONE = ':cic.phone'
    PREFERENCES = ':cic.preferences'
    STATEMENT = ':cic.statement'
    TOKEN_DATA = ':cic.token.data'
    TOKEN_DEFAULT = ':cic.token.default'
    TOKEN_META = ':cic.token.meta'
    TOKEN_META_SYMBOL = ':cic.token.meta.symbol'
    TOKEN_PROOF = ':cic.token.proof'
    TOKEN_PROOF_SYMBOL = ':cic.token.proof.symbol'
