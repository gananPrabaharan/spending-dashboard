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
                         ["transactionId", "date", "description", "amount", "categoryId"],
                         ["INTEGER", "DATE", "NVARCHAR", "NUMERIC", "INTEGER", "INTEGER"])

    CATEGORIES = Table("Categories",
                       ["categoryId", "name"],
                       ["INTEGER", "NVARCHAR UNIQUE"])
