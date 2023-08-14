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


def insert_multiple(table, row_list, existing_term=None, extra_string=None):
    """
    Insert multiple rows into a table

    :param table: Table object
    :param row_list: list of lists, with each inner list representing values for a single entry
    :param existing_term: (optional string) SQL term to use if value exists in db
    :param extra_string: (optional string) extra portion of query to add
    :return:
    """
    if len(row_list) == 0:
        return

    table_columns = list(table.column_mapping.keys())
    if len(row_list[0]) == len(table_columns) - 1:
        column_string = ", ".join([col for col in table_columns[1:]])
    elif len(row_list[0]) == len(table_columns):
        column_string = ", ".join([col for col in table_columns])
    else:
        print(len(table_columns))
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

    if extra_string is not None:
        query += extra_string

    execute_query(query)


def create_tables():
    """
    Create necessary Tables

    :return:
    """
    execute_query(Tables.TRANSACTIONS.create_query)
    execute_query(Tables.CATEGORIES.create_query)
    insert_multiple(Tables.CATEGORIES, [[-1, 0, ""]], "IGNORE")
    insert_multiple(Tables.CATEGORIES, [[0, 1000, "Payments"]], "IGNORE")
    execute_query(Tables.VENDORS.create_query)
    execute_query(Tables.VENDOR_CATEGORIES.create_query)
    execute_query(Tables.NEW_VENDORS.create_query)


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
    delete_table(Tables.VENDORS.name)
    delete_table(Tables.VENDOR_CATEGORIES.name)
    delete_table(Tables.NEW_VENDORS.name)


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


def retrieve_from_table(table, extra_query=None):
    """
    Retrieve rows from table as list of dictionaries

    :param table: Table object
    :param extra_query: string containing extra conditions on retrieve query
    :return: List of dictionaries of format (key, value)->(column_name, column_value)
             representing row values. First column name is replaced to "id" for ease of front end table
    """
    # Create query
    table_columns = list(table.column_mapping.keys())
    column_string = ", ".join(table_columns)
    query = "SELECT " + column_string + " FROM " + table.name
    if extra_query is not None:
        query += " " + extra_query

    # Get query result
    query_result = execute_query(query, True)

    # Assemble list of dictionaries for each row
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
    """
    Delete query for table

    :param table: Table object to delete from
    :param condition: (string) Condition to delete on
    :param value: (any) value to add to condition
    :return:
    """
    query = "DELETE FROM " + table.name + " WHERE "
    query += condition + get_value(value)
    execute_query(query)


def insert_transactions(transaction_list):
    """
    Insert list of transactions into transaction table

    :param transaction_list: list of transaction objects
    :return:
    """
    # Create insertion values
    transaction_input = []
    for transaction in transaction_list:
        row_values = [
            transaction.trans_id,
            transaction.date,
            transaction.description,
            transaction.amount,
            transaction.category_id,
            transaction.vendor_id
        ]
        transaction_input.append(row_values)

    # insert transactions in to table
    insert_multiple(Tables.TRANSACTIONS, transaction_input, "REPLACE")


def find_transaction(transaction):
    """
    Check whether a transaction has already been inserted (without using transaction id)
    :param transaction: Transaction object
    :return: list of transaction ids corresponding to matching transactions
    """
    query = "SELECT transactionId from " + Tables.TRANSACTIONS.name + " " + \
            "WHERE date=" + get_value(transaction.date) + " " + \
            "AND description=" + get_value(transaction.description) + " " + \
            "AND amount=" + get_value(transaction.amount)

    results = execute_query(query, True)
    transaction_ids = []
    for row in results:
        transaction_ids.append(row[0])

    return transaction_ids


def insert_vendor_categories_changes(changes_list):
    """
    Insert changes to vendor categories table

    :param changes_list: nested list of changes. inner list format: [old_vend_id, old_cat_id, new_vend_id, new_cat_id]
    :return:
    """

    # Keep track of updates to vendor id + category id combinations
    updates_dict = {}
    for old_vend_id, old_cat_id, new_vend_id, new_cat_id in changes_list:
        old_tuple = (old_vend_id, old_cat_id)
        new_tuple = (new_vend_id, new_cat_id)

        if old_vend_id != -1 and old_cat_id != -1:
            updates_dict[old_tuple] = updates_dict.get(old_tuple, 0) - 1

        if new_vend_id != -1 and new_cat_id != -1:
            updates_dict[new_tuple] = updates_dict.get(new_tuple, 0) + 1

    # Create list of rows to update table with (1 insert per change)
    increment_items = []
    decrement_items = []
    for key, change in updates_dict.items():
        vend_id, cat_id = key
        for i in range(abs(change)):
            if change < 0:
                decrement_items.append([vend_id, cat_id, -1])
            elif change > 0:
                increment_items.append([vend_id, cat_id, 1])

    print(increment_items)
    print(decrement_items)
    # Insert into table
    increment_string = " ON CONFLICT(vendorId, categoryId) DO UPDATE SET count=count+1"
    insert_multiple(Tables.VENDOR_CATEGORIES, increment_items, extra_string=increment_string)

    decrement_string = " ON CONFLICT(vendorId, categoryId) DO UPDATE SET count=count-1"
    insert_multiple(Tables.VENDOR_CATEGORIES, decrement_items, extra_string=decrement_string)


def insert_new_vendor_categories_changes(changes_list):
    """
    Insert changes to vendor categories table

    :param changes_list: nested list of changes. inner list format: [old_vend_id, old_cat_id, new_vend_id, new_cat_id]
    :return:
    """

    vendor_query = "SELECT NewVendors.vendorId, NewVendors.vendorName, NewVendors.categoryId " \
                            "FROM NewVendors "
    vendor_results = execute_query(vendor_query, True)
    vendor_name_mapping = {}
    for vendor_id, vendor_name, cat_id in vendor_results:
        vendor_name_mapping[vendor_id] = vendor_name

    changes_insert = []
    for vendor_id, category_id in changes_list:
        changes_insert.append([vendor_id, vendor_name_mapping[vendor_id], category_id])

    insert_multiple(Tables.NEW_VENDORS, changes_insert, "REPLACE")


def db_setup():
    if not os.path.exists(Paths.DATABASE):
        Path(Paths.DATABASE).mkdir(parents=True, exist_ok=False)
    create_tables()


if __name__ == "__main__":
    # delete_all_tables()

    # date_query = "SELECT * FROM Transactions WHERE date >= '2021-05-18' and date <= '2021-05-20'"
    # temp_query = 'select categoryId, name, budget from "Categories"'


    execute_query(Tables.NEW_VENDORS.create_query)
    vendor_category_query = "SELECT Vendors.vendorId, Vendors.vendorName, Categories.categoryId " \
                            "FROM Vendors " \
                            "JOIN VendorCategories " \
                            "ON Vendors.vendorId = VendorCategories.vendorId " \
                            "JOIN Categories " \
                            "ON Categories.categoryId = VendorCategories.categoryId"

    vendor_category_results = execute_query(vendor_category_query, True)
    new_vendor_inserts = []
    for vendor_id, vendor_name, cat_id in vendor_category_results:
        new_vendor_inserts.append([vendor_id, vendor_name, cat_id])


    # insert_multiple(Tables.NEW_VENDORS, new_vendor_inserts)
    temp_query = "SELECT * FROM NewVendors where NewVendors.categoryId != -1;"
    results = execute_query(temp_query, True)
    print(results)

    temp_query = "SELECT * FROM Categories;"
    results = execute_query(temp_query, True)
    print(results)



