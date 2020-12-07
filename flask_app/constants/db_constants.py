class Table:
    def __init__(self, name, columns, data_types):
        self.name = name
        self.columns = columns
        self.id_col = columns[0]
        self.get_create_query(data_types)
        self.create_query = self.get_create_query(data_types)

    def get_create_query(self, data_types):
        query = "CREATE TABLE IF NOT EXISTS " + self.name + " ("

        column_strings = [self.id_col + " " + data_types[0] + " PRIMARY KEY"]
        for i in range(1, len(self.columns)):
            col_string = self.columns[i] + " " + data_types[i]
            column_strings.append(col_string)

        query += ", ".join(column_strings) + ")"
        return query


class Tables:
    TRANSACTIONS = Table("Transactions",
                         ["transactionId", "date", "description", "amount"],
                         ["INTEGER", "DATE", "NVARCHAR", "NUMERIC", "INTEGER"])

    CATEGORIES = Table("Categories",
                       ["categoryId", "name"],
                       ["INTEGER", "NVARCHAR UNIQUE"])

    # TRANSACTIONS = {
    #     "name": "Transactions",
    #     "columns": ["transactionId", "date", "description", "amount"],
    #     "id_col": "transactionId"
    # }
    #
    # CATEGORIES = {
    #     "name": "Categories",
    #     "columns": ["categoryId", "name"]
    # }


# class TableDefinitions:
#     TRANSACTION_DB_QUERY = "CREATE TABLE IF NOT EXISTS " + Tables.TRANSACTIONS["name"] + " " \
#                                                                                          "(transactionId INTEGER PRIMARY KEY, " \
#                                                                                          "date DATE, " \
#                                                                                          "description NVARCHAR, " \
#                                                                                          "amount NUMERIC, " \
#                                                                                          "categoryId INTEGER" \
#                                                                                          ") "
#
#     CATEGORIES_DB_QUERY = "CREATE TABLE IF NOT EXISTS " + Tables.CATEGORIES["name"] + " " \
#                                                                                       "(categoryId INTEGER PRIMARY KEY, " \
#                                                                                       "name NVARCHAR UNIQUE" \
#                                                                                       ") "
