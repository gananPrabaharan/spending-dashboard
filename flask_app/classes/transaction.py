from constants.general_constants import Columns


class Transaction:
    def __init__(self, trans_id=None, trans_date=None, description=None, category=None, amount=None):
        self.trans_id = trans_id
        self.date = trans_date
        self.description = description
        self.category = category
        self.amount = amount

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

        category = ""
        return cls(trans_id, date, description, category, amount)

    @classmethod
    def from_db(cls, trans_dict, category_mapping):
        trans_id = trans_dict["id"]
        date = trans_dict["date"]
        description = trans_dict["description"]
        amount = trans_dict["amount"]
        category_id = trans_dict["categoryId"]
        category = category_mapping.get(category_id, "")
        return cls(trans_id, date, description, category, amount)

    @classmethod
    def parse_from_db(cls, row_tuple, category_mapping):
        trans_id = row_tuple[0]
        date = row_tuple[1]
        description = row_tuple[2]
        amount = row_tuple[3]
        category_id = row_tuple[4]
        category = category_mapping.get(category_id, "")

        return cls(trans_id, date, description, category, amount)

    def to_dict(self):
        trans_dict = {
            Columns.TRANSACTION_ID: self.trans_id,
            Columns.DATE: self.date,
            Columns.DESCRIPTION: self.description,
            Columns.CATEGORY: self.category,
            Columns.AMOUNT: self.amount
        }
        return trans_dict

    @classmethod
    def from_dict(cls, trans_dict):
        transaction = cls(trans_id=trans_dict[Columns.TRANSACTION_ID],
                          trans_date=trans_dict[Columns.DATE],
                          description=trans_dict[Columns.DESCRIPTION],
                          category=trans_dict[Columns.CATEGORY],
                          amount=trans_dict[Columns.AMOUNT]
                          )
        return transaction
