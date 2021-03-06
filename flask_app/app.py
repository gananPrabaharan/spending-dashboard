from flask import Flask, request, jsonify
from flask_cors import CORS
from classes.transaction import Transaction
from constants.general_constants import Deployment
from constants.db_constants import Tables, DEFAULT_ID
from services.utilities import transform_df, dataframe_to_transactions, filter_new_transactions
from services.db_utilities import retrieve_from_table, db_setup, insert_multiple, delete_from_table, \
    retrieve_table_mapping, insert_transactions, execute_query, insert_vendor_categories_changes
from services.category_classification import categorize_vendors
from rule_based_named_entity_recognition.ner import get_vendors_list

import pandas as pd
import json

app = Flask(__name__)
CORS(app)


@app.route('/api/parseFile', methods=["POST"])
def parse_file():
    input_file = request.files["fileInput"]
    transactions_df = pd.read_csv(input_file, header=None)
    transactions_df = transform_df(transactions_df)
    transaction_list = dataframe_to_transactions(transactions_df)
    transaction_dict_list = [t.to_dict() for t in transaction_list]
    return jsonify(transaction_dict_list)


@app.route('/api/import', methods=["POST"])
def import_transactions():
    transaction_dict_list = request.form["transactions"]
    if transaction_dict_list is not None:
        # convert input to list of Transaction objects
        transaction_dict_list = json.loads(transaction_dict_list)
        transaction_list = [Transaction.from_dict(t) for t in transaction_dict_list]

        # Filer transactions to keep only new ones
        transactions_to_add = filter_new_transactions(transaction_list)

        # Get vendor memos that haven't been seen before
        new_vendor_memos = []
        for trans in transactions_to_add:
            new_vendor_memos.append(trans.description)

        # Maps memo to extracted name
        transaction_memo_name_mapping = get_vendors_list(new_vendor_memos)

        # Get vendor names that haven't been seen before
        vendors_to_add = [[name] for name in transaction_memo_name_mapping.values()]

        # Insert vendors and retrieve new memo to id mapping
        insert_multiple(Tables.VENDORS, vendors_to_add, "IGNORE")
        vendor_name_id_mapping = retrieve_table_mapping(Tables.VENDORS, "vendorName", "vendorId")

        # Assemble values to insert into database
        for transaction in transactions_to_add:
            # Assemble rows to be inserted into DB
            vendor_name = transaction_memo_name_mapping[transaction.description]
            transaction.vendor_id = vendor_name_id_mapping[vendor_name]

        insert_transactions(transactions_to_add)
    return jsonify(transaction_dict_list)


@app.route('/api/transactions', methods=["GET", "POST"])
def transactions():
    if request.method == "GET":
        # Retrieve transactions from table
        start_date = request.args.get("startDate")
        end_date = request.args.get("endDate")
        date_condition = ""
        if start_date is not None:
            date_condition += "WHERE date >= '" + start_date + "'"

        if end_date is not None:
            date_condition += " AND date <= '" + end_date + "'"

        transaction_rows = retrieve_from_table(Tables.TRANSACTIONS, date_condition)
        transaction_list = [Transaction.from_db(row) for row in transaction_rows]
        transaction_dict_list = [t.to_dict() for t in transaction_list]
        return jsonify(transaction_dict_list), 200
    else:
        transaction_dict_list = json.loads(request.form["transactions"])
        vendor_cat_changes = json.loads(request.form["changes"])

        # Assemble input for recording changes made to vendor or category
        changes_list = []
        for old_vend_id, old_cat_id, new_vend_id, new_cat_id in vendor_cat_changes.values():
            if old_vend_id != new_vend_id or old_cat_id != new_cat_id:
                old_vend_id = int(old_vend_id)
                old_cat_id = int(old_cat_id)
                new_vend_id = int(new_vend_id)
                new_cat_id = int(new_cat_id)

                changes_list.append([old_vend_id, old_cat_id, new_vend_id, new_cat_id])

        # Update vendor_categories table if necessary
        if len(changes_list) > 0:
            insert_vendor_categories_changes(changes_list)

        # Insert transaction changes into table
        transaction_rows = []
        for trans_dict in transaction_dict_list:
            trans_id = trans_dict["id"]
            trans_date = trans_dict["date"]
            description = trans_dict["description"]
            amount = trans_dict["amount"]
            category_id = trans_dict["categoryId"]
            vendor_id = trans_dict["vendorId"]

            curr_row = [trans_id, trans_date, description, amount, category_id, vendor_id]
            transaction_rows.append(curr_row)

        insert_multiple(Tables.TRANSACTIONS, transaction_rows, "REPLACE")
    return "success", 200


@app.route('/api/categorize', methods=["POST"])
def categorize():
    # Convert input to transaction objects
    transaction_dict_list = json.loads(request.form["transactionList"])
    transaction_list = [Transaction.from_dict(t) for t in transaction_dict_list]

    # Identify vendor ids that need to be categorized
    vendor_ids_to_categorize = []
    for trans in transaction_list:
        if trans.category_id is not None and trans.category_id == DEFAULT_ID:
            vendor_ids_to_categorize.append(trans.vendor_id)

    # Categorize vendor ids
    vendor_id_category_id_mapping = categorize_vendors(vendor_ids_to_categorize)

    # Keep track of changes to insert into vendor_category table
    vendor_category_changes = []

    # Update necessary transactions
    updated_transactions = []
    for trans in transaction_list:
        if trans.category_id is not None and trans.category_id == DEFAULT_ID:
            vendor_id = trans.vendor_id
            category_id = vendor_id_category_id_mapping.get(vendor_id, "")
            if category_id != DEFAULT_ID:
                # Record change
                vendor_category_changes.append([vendor_id, trans.category_id, vendor_id, category_id])

                # Update transaction
                trans.category_id = category_id
                updated_transactions.append(trans)

    # Update DB
    insert_vendor_categories_changes(vendor_category_changes)
    insert_transactions(updated_transactions)

    # Convert transactions into dictionaries
    transaction_dict_list = [t.to_dict() for t in transaction_list]

    return jsonify(transaction_dict_list), 200


@app.route('/api/categories', methods=["GET", "POST", "DELETE"])
def get_categories():
    if request.method == "POST":
        # Adding category to DB
        category_id = request.form.get("categoryId")
        category_name = json.loads(request.form["categoryName"])
        category_budget = json.loads(request.form["categoryBudget"])
        
        # Assemble values for inserting into DB
        if category_id is None:
            category_values = [category_budget, category_name]
        else:
            category_id = json.loads(category_id)
            category_values = [category_id, category_budget, category_name]

        insert_multiple(Tables.CATEGORIES, [category_values], "REPLACE")
    elif request.method == "DELETE":
        # Delete category from DB
        category_id = json.loads(request.form["categoryId"])
        condition = "categoryId="
        delete_from_table(Tables.CATEGORIES, condition, category_id)
        update_query = "update " + Tables.TRANSACTIONS.name + " set categoryId='" + str(DEFAULT_ID) + \
                       "' where categoryId='" + category_id + "'"
        execute_query(update_query)

    category_query = "SELECT " + ", ".join(Tables.CATEGORIES.columns) + " FROM " + Tables.CATEGORIES.name
    category_results = execute_query(category_query, True)
    category_dict = {}
    for cat_id, cat_budget, cat_name in category_results:
        category_dict[cat_id] = {"name": cat_name, "budget": cat_budget} 

    return jsonify(category_dict)


if __name__ == "__main__":
    db_setup()
    app.run(Deployment.HOST, Deployment.FLASK_PORT, debug=False)
