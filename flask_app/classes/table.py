class Table:
    def __init__(self, name, column_mapping, primary_key_column=None):
        self.name = name
        self.column_mapping = column_mapping
        self.create_query = self.get_create_query(primary_key_column)

    def get_create_query(self, primary_key_column=None):
        query = "CREATE TABLE IF NOT EXISTS " + self.name + " ("

        column_strings = []
        for column, sql_type in self.column_mapping.items():
            col_string = column + " " + sql_type
            column_strings.append(col_string)

        if primary_key_column is not None:
            column_strings.append(primary_key_column)

        query += ", ".join(column_strings) + ")"
        return query
