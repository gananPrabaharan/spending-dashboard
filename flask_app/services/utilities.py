from constants.general_constants import Columns
from services.db_utilities import find_transaction, retrieve_from_table
from classes.transaction import Transaction
from constants.db_constants import Tables


def transform_df(transactions_df):
    """
    Adds column names to DataFrame

    :param transactions_df: DataFrame of transactions
    :return: DataFrame with column names
    """
    transactions_df.columns = [Columns.DATE, Columns.DESCRIPTION, Columns.WITHDRAWAL, Columns.DEPOSIT, Columns.ACCOUNT]
    transactions_df.fillna("", inplace=True)
    return transactions_df


def dataframe_to_transactions(transactions_df):
    transactions_list = []
    index = 0
    for row_tuple in transactions_df.itertuples():
        amount = getattr(row_tuple, Columns.DEPOSIT)
        if amount is None or (type(amount) == str and len(amount) == 0):
            amount = getattr(row_tuple, Columns.WITHDRAWAL)
            amount = -float(amount)
        else:
            amount = float(amount)

        trans_date = getattr(row_tuple, Columns.DATE)
        description = getattr(row_tuple, Columns.DESCRIPTION)

        transaction = Transaction(trans_id=index,
                                  trans_date=trans_date,
                                  description=description,
                                  category_id=-1,
                                  amount=amount)
        transactions_list.append(transaction)
        index += 1

    return transactions_list


def filter_new_transactions(transaction_list):
    """
    Given a list of transactions, find the ones that aren't in the database

    :param transaction_list: list of Transaction objects
    :return: list of Transaction objects not already in database
    """
    used_ids = set()
    new_transactions = []
    for transaction in transaction_list:
        transaction_ids = find_transaction(transaction)
        new_flag = True

        # See if any matching transactions exist in DB
        for trans_id in transaction_ids:
            # Make sure transaction is not double counted
            if trans_id not in used_ids:
                used_ids.add(trans_id)
                new_flag = False
                break

        if new_flag:
            new_transactions.append(transaction)

    return new_transactions


def get_transactions_for_frontend(date_condition=None):
    transaction_rows = retrieve_from_table(Tables.TRANSACTIONS, date_condition)
    transaction_list = [Transaction.from_db(row) for row in transaction_rows]
    transaction_dict_list = [t.to_dict() for t in transaction_list]
    transaction_dict_list = sorted(transaction_dict_list, key=lambda x: x['date'], reverse=True)
    return transaction_dict_list
