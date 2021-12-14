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
    TOKEN_ACTIVE = ':cic.token.active'
    TOKEN_DATA = ':cic.token.data'
    TOKEN_DATA_LIST = ':cic.token.data.list'
    TOKEN_DEFAULT = ':cic.token.default'
    TOKEN_LAST_RECEIVED = ':cic.token.last.received'
    TOKEN_LAST_SENT = ':cic.token.last.sent'
    TOKEN_META = ':cic.token.meta'
    TOKEN_META_SYMBOL = ':cic.token.meta.symbol'
    TOKEN_PROOF = ':cic.token.proof'
    TOKEN_PROOF_SYMBOL = ':cic.token.proof.symbol'
    TOKEN_SYMBOLS_LIST = ':cic.token.symbols.list'
