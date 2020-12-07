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
    if len(row_list[0]) == len(table.columns) - 1:
        column_string = ", ".join([col for col in table.columns[1:]])
    elif len(row_list[0]) == len(table.columns):
        column_string = ", ".join([col for col in table.columns])
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


def retrieve_categories():
    columns = ", ".join(Tables.CATEGORIES.columns)
    query = "SELECT " + columns + " FROM " + Tables.CATEGORIES.name

    query_result = execute_query(query, True)

    cat_dict_list = []
    for cat_id, cat_name in query_result:
        cat_dict_list.append({
            "id": cat_id,
            "name": cat_name
        })

    return cat_dict_list


def retrieve_from_table(table):
    column_string = ", ".join(table.columns)
    query = "SELECT " + column_string + " FROM " + table.name

    query_result = execute_query(query, True)

    item_dict_list = []
    for result_tuple in query_result:
        item_dict = {
            "id": result_tuple[0]
        }
        for index in range(1, len(table.columns)):
            column_name = table.columns[index]
            item_dict[column_name] = result_tuple[index]

        item_dict_list.append(item_dict)

    return item_dict_list


def delete_from_table(table, condition, value):
    query = "DELETE FROM " + table.name + " WHERE "
    query += condition + get_value(value)
    execute_query(query)


def update_table(table, items_list):
    for item_dict in items_list:
        query = "UPDATE " + table.name + " SET "

        col_values = []
        for i in range(len(table.columns)):
            col_name = table.columns[i]
            value = get_value(item_dict[col_name])
            col_string = col_name + " = " + get_value(value)
            col_values.append(col_string)

        query += ", ".join(col_values) + " "
        query += "WHERE " + table.id_col + " = " + get_value(item_dict["id"])


    return


def db_setup():
    if not os.path.exists(Paths.DATABASE):
        Path(Paths.DATABASE).mkdir(parents=True, exist_ok=False)
    create_tables()


if __name__ == "__main__":
    delete_all_tables()
