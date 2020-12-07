from flask import Flask, request, jsonify
from flask_cors import CORS
from constants.general_constants import Deployment
from constants.db_constants import Tables
from services.utilities import transform_df, transactions_to_dict
from services.db_utilities import retrieve_from_table, db_setup, insert_multiple, delete_from_table, update_table

import pandas as pd
import json

app = Flask(__name__)
CORS(app)


@app.route('/api/import', methods=["POST"])
def import_transactions():
    input_file = request.files["file_input"]
    transactions_df = pd.read_csv(input_file, header=None)
    transactions_df = transform_df(transactions_df)
    transaction_dict_list = transactions_to_dict(transactions_df)
    return jsonify(transaction_dict_list)


@app.route('/api/transactions', methods=["GET", "POST"])
def transactions():
    if request.method == "GET":
        category_dict_list = retrieve_from_table(Tables.TRANSACTIONS)
        return jsonify(category_dict_list), 200
    else:
        transaction_list = json.loads(request.form["transactionList"])
        insert_multiple(Tables.TRANSACTIONS, transaction_list, "REPLACE")
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
