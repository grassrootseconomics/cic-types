# standard imports
import enum
import logging
import datetime

logg = logging.getLogger(__name__)


class TokenTxType(enum.Enum):
    faucet_giveto = 'faucet.give_to'
    erc20_transfer = 'erc20.transfer'


class TokenTx:

    def __init__(self):
        self.sender = None
        self.recipient = None
        self.source_token = None
        self.destination_token = None
        self.to_value = None
        self.from_value = None
        self.block_number = None
        self.tx_hash = None
        self.tx_index = None
        self.tx_type = None
        self.date_block = None
        self.success = None

        self.source_token_label = None
        self.destination_token_label = None
        self.sender_label = None
        self.recipient_label = None
        self.from_value_label = None
        self.to_value_label = None


    @classmethod
    def from_dict(cls, tx_src):
        tx = cls()
        for k in tx_src.keys():
            v = tx_src[k]
            if k == 'tx_type':
                v = TokenTxType(v)
            elif not hasattr(tx, k):
                logg.warning('skipping invalid attribute {}'.format(k))
                continue
            setattr(tx, k, tx_src[k])

        tx.sender_label = tx.sender
        tx.recipient_label = tx.recipient
        tx.source_token_label = tx.source_token
        tx.destination_token_label = tx.destination_token
        tx.from_value_label = tx.from_value
        tx.to_value_label = tx.to_value

        tx.date_block_label = datetime.datetime.fromtimestamp(tx.date_block).ctime()

        return tx


    def __str__(self):
        return 'TokenTx: {} from {} token {} value {} to {} token {} value {} block {} tx {} result {}'.format(
                self.date_block_label,
                self.sender_label,
                self.source_token_label,
                self.from_value_label,
                self.recipient_label,
                self.destination_token_label,
                self.to_value_label,
                self.block_number,
                self.tx_hash,
                self.success,
                )
