from flask import Flask, request, jsonify
from flask_cors import CORS
from classes.transaction import Transaction
from constants.general_constants import Deployment
from constants.db_constants import Tables
from services.utilities import transform_df, dataframe_to_transactions, filter_new_transactions
from services.db_utilities import retrieve_from_table, db_setup, insert_multiple, delete_from_table, retrieve_table_mapping
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
        vendor_memo_id_mapping = retrieve_table_mapping(Tables.VENDORS, "vendorMemo", "vendorId")
        vendor_name_id_mapping = retrieve_table_mapping(Tables.VENDORS, "vendorName", "vendorId")

        # Get vendor memos that haven't been seen before
        new_vendor_memos = []
        for trans in transactions_to_add:
            if trans.description not in vendor_memo_id_mapping:
                new_vendor_memos.append(trans.description)

        # Maps memo to extracted name
        transaction_memo_name_mapping = get_vendors_list(new_vendor_memos)

        # Get vendor names that haven't been seen before
        vendors_to_add = []
        for memo, name in transaction_memo_name_mapping.items():
            if name not in vendor_name_id_mapping:
                vendors_to_add.append([memo, name, ""])

        # Insert vendors and retrieve new memo to id mapping
        insert_multiple(Tables.VENDORS, vendors_to_add, "IGNORE")
        vendor_memo_id_mapping = retrieve_table_mapping(Tables.VENDORS, "vendorMemo", "vendorId")

        # Assemble values to insert into database
        category_mapping = retrieve_table_mapping(Tables.CATEGORIES, "name", "categoryId")
        transaction_input = []
        for transaction in transactions_to_add:
            # Assemble rows to be inserted into DB
            row_values = [
                transaction.trans_id,
                transaction.date,
                transaction.description,
                transaction.amount,
                category_mapping.get(transaction.category, 0)       # Default category_id is 0
            ]
            transaction_input.append(row_values)

        insert_multiple(Tables.TRANSACTIONS, transaction_input)
    return jsonify(transaction_dict_list)


@app.route('/api/transactions', methods=["GET", "POST"])
def transactions():
    if request.method == "GET":
        category_mapping = retrieve_table_mapping(Tables.CATEGORIES, "categoryId", "name")
        transaction_rows = retrieve_from_table(Tables.TRANSACTIONS)
        transaction_list = [Transaction.from_db(row, category_mapping) for row in transaction_rows]
        transaction_dict_list = [t.to_dict() for t in transaction_list]
        return jsonify(transaction_dict_list), 200
    else:
        category_mapping = retrieve_table_mapping(Tables.CATEGORIES, "name", "categoryId")
        transaction_dict_list = json.loads(request.form["transactions"])
        transaction_rows = []
        for trans_dict in transaction_dict_list:
            trans_id = trans_dict["id"]
            trans_date = trans_dict["date"]
            description = trans_dict["description"]
            amount = trans_dict["amount"]
            category = trans_dict["category"]
            category_id = category_mapping.get(category, 0)

            curr_row = [trans_id, trans_date, description, amount, category_id]
            transaction_rows.append(curr_row)

        insert_multiple(Tables.TRANSACTIONS, transaction_rows, "REPLACE")
    return "success", 200


@app.route('/api/categories', methods=["GET", "POST", "DELETE"])
def get_categories():
    if request.method == "POST":
        category = json.loads(request.form["categoryToAdd"])
        insert_multiple(Tables.CATEGORIES, [[category]], "IGNORE")
    elif request.method == "DELETE":
        category_id = json.loads(request.form["categoryId"])
        condition = "categoryId="
        delete_from_table(Tables.CATEGORIES, condition, category_id)

    category_dict_list = retrieve_from_table(Tables.CATEGORIES)
    return jsonify(category_dict_list)


if __name__ == "__main__":
    db_setup()
    app.run(Deployment.HOST, Deployment.FLASK_PORT, debug=False)
