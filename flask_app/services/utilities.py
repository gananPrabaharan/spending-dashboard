from constants.general_constants import Columns


def transform_df(transactions_df):
    transactions_df.columns = [Columns.DATE, Columns.DESCRIPTION, Columns.WITHDRAWAL, Columns.DEPOSIT, Columns.ACCOUNT]
    transactions_df.fillna("", inplace=True)
    return transactions_df


def transactions_to_dict(transactions_df):
    transactions_dict_list = []
    index = 0
    for row_tuple in transactions_df.itertuples():
        row_dict = {
            Columns.TRANSACTION_ID: index,
            Columns.DATE: getattr(row_tuple, Columns.DATE),
            Columns.DESCRIPTION: getattr(row_tuple, Columns.DESCRIPTION),
            Columns.WITHDRAWAL: getattr(row_tuple, Columns.WITHDRAWAL),
            Columns.DEPOSIT: getattr(row_tuple, Columns.DEPOSIT),
            Columns.CATEGORY: ""
        }
        transactions_dict_list.append(row_dict)
        index += 1

    return transactions_dict_list
