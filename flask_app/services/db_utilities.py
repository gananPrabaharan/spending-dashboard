import sqlite3
from constants.db_constants import Tables
from constants.general_constants import Database, Paths
import os
from pathlib import Path


def get_value(value):
    """
    Converts a value to make it read for a SQL query
    :param value: value to convert
    :return: (string) value converted to use in a SQL query
    """
    if type(value) == str:
        # escape single quotes with two single quotes
        # if the value is a string, we need to wrap it in single quotes
        return "'" + value.replace("'", "''") + "'"
    else:
        return str(value)


def insert_multiple(table, row_list, existing_term=None):
    """
    Insert multiple rows into a table

    :param table: Table object
    :param row_list: list of lists, with each inner list representing values for a single entry
    :param existing_term: (string) SQL term to use if value exists in db
    :return:
    """
    table_columns = list(table.column_mapping.keys())
    if len(row_list[0]) == len(table_columns) - 1:
        column_string = ", ".join([col for col in table_columns[1:]])
    elif len(row_list[0]) == len(table_columns):
        column_string = ", ".join([col for col in table_columns])
    else:
        raise ValueError

    if existing_term is not None:
        query = "INSERT OR " + existing_term + " "
    else:
        query = "INSERT "

    query += "INTO " + table.name + "(" + column_string + ") "
    query += "VALUES "

    row_inserts = []
    for row_values in row_list:
        row_string = "("
        row_string += ", ".join([get_value(value) for value in row_values])
        row_string += ")"
        row_inserts.append(row_string)

    query += ", ".join(row_inserts)
    execute_query(query)


def create_tables():
    """
    Create necessary Tables

    :return:
    """
    execute_query(Tables.TRANSACTIONS.create_query)
    execute_query(Tables.CATEGORIES.create_query)
    insert_multiple(Tables.CATEGORIES, [[0, ""]], "IGNORE")


def delete_table(table_name):
    """
    Delete a table

    :param table_name: (string) table to delete
    :return:
    """
    query = "DROP TABLE IF EXISTS " + table_name
    execute_query(query)


def delete_all_tables():
    """
    Delete all tables
    :return:
    """
    delete_table(Tables.TRANSACTIONS.name)
    delete_table(Tables.CATEGORIES.name)


def execute_query(query, select_flag=False):
    """
    General function for executing queries

    :param query: (string) query to execute
    :param select_flag: (bool) flag indicating whether we are expecting some output
    :return:
    """
    result = None

    conn = sqlite3.connect(Database.CONNECTION)
    c = conn.cursor()
    c.execute(query)

    if select_flag:
        result = c.fetchall()

    conn.commit()
    c.close()
    conn.close()

    return result


def retrieve_table_mapping(table, key_column, value_column):
    """
    Retrieve dictionary mapping one column to another
    :param table: table object
    :param key_column: column to use as dictionary key
    :param value_column: column to use as dictionary value
    :return: dictionary mapping keyColumn to valueColumn
    """
    columns = key_column + ", " + value_column
    query = "SELECT " + columns + " FROM " + table.name
    query_result = execute_query(query, True)

    table_dict = {}
    for key, value in query_result:
        table_dict[key] = value

    return table_dict


def retrieve_from_table(table):
    table_columns = list(table.column_mapping.keys())
    column_string = ", ".join(table_columns)
    query = "SELECT " + column_string + " FROM " + table.name

    query_result = execute_query(query, True)

    item_dict_list = []
    for result_tuple in query_result:
        item_dict = {
            "id": result_tuple[0]
        }
        for index in range(1, len(table_columns)):
            column_name = table_columns[index]
            item_dict[column_name] = result_tuple[index]

        item_dict_list.append(item_dict)

    return item_dict_list


def delete_from_table(table, condition, value):
    query = "DELETE FROM " + table.name + " WHERE "
    query += condition + get_value(value)
    execute_query(query)


def find_transaction(transaction):
    query = "SELECT transactionId from " + Tables.TRANSACTIONS.name + " " + \
            "WHERE date=" + get_value(transaction.date) + " " + \
            "AND description=" + get_value(transaction.description) + " " + \
            "AND amount=" + get_value(transaction.amount)

    results = execute_query(query, True)
    transaction_ids = []
    for row in results:
        transaction_ids.append(row[0])

    return transaction_ids


def db_setup():
    if not os.path.exists(Paths.DATABASE):
        Path(Paths.DATABASE).mkdir(parents=True, exist_ok=False)
    create_tables()


if __name__ == "__main__":
    delete_all_tables()
