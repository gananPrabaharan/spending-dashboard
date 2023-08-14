from constants.general_constants import Columns


class Transaction:
    def __init__(self, trans_id=None, trans_date=None, description=None, category_id=None, amount=None, vendor_id=-1):
        self.trans_id = trans_id
        self.date = trans_date
        self.description = description
        self.category_id = category_id
        self.amount = amount
        self.vendor_id = vendor_id

    @classmethod
    def from_tuple(cls, named_tuple, trans_id=None):
        date = getattr(named_tuple, Columns.DATE)
        description = getattr(named_tuple, Columns.DESCRIPTION)
        amount = getattr(named_tuple, Columns.DEPOSIT)
        if amount is None:
            amount = getattr(named_tuple, Columns.WITHDRAWAL)
            amount = -float(amount)
        else:
            amount = float(amount)

        category_id = -1
        vendor_id = -1
        return cls(trans_id, date, description, category_id, amount, vendor_id)

    @classmethod
    def from_db(cls, trans_dict):
        trans_id = trans_dict["id"]
        date = trans_dict["date"]
        description = trans_dict["description"]
        category_id = trans_dict["categoryId"]
        amount = trans_dict["amount"]
        vendor_id = trans_dict["vendorId"]
        return cls(trans_id, date, description, category_id, amount, vendor_id)

    @classmethod
    def parse_from_db(cls, row_tuple):
        trans_id = row_tuple[0]
        date = row_tuple[1]
        description = row_tuple[2]
        amount = row_tuple[3]
        category_id = row_tuple[4]
        vendor_id = row_tuple[5]
        return cls(trans_id, date, description, category_id, amount, vendor_id)

    def to_dict(self):
        trans_dict = {
            Columns.TRANSACTION_ID: self.trans_id,
            Columns.DATE: self.date,
            Columns.DESCRIPTION: self.description,
            Columns.CATEGORY_ID: self.category_id,
            Columns.AMOUNT: self.amount,
            Columns.VENDOR_ID: self.vendor_id
        }
        return trans_dict

    @classmethod
    def from_dict(cls, trans_dict):
        transaction = cls(trans_id=trans_dict[Columns.TRANSACTION_ID],
                          trans_date=trans_dict[Columns.DATE],
                          description=trans_dict[Columns.DESCRIPTION],
                          category_id=trans_dict[Columns.CATEGORY_ID],
                          amount=trans_dict[Columns.AMOUNT],
                          vendor_id=trans_dict[Columns.VENDOR_ID]
                          )
        return transaction

    @staticmethod
    def dict_to_db_insert(trans_dict):
        return [
            trans_dict[Columns.TRANSACTION_ID],
            trans_dict[Columns.DATE],
            trans_dict[Columns.DESCRIPTION],
            trans_dict[Columns.AMOUNT],
            trans_dict[Columns.CATEGORY_ID],
            trans_dict[Columns.VENDOR_ID]
        ]

