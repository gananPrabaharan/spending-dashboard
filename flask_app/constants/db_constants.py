from classes.table import Table


class Tables:
    TRANSACTIONS = Table(name="Transactions",
                         column_mapping={
                             "transactionId": "INTEGER PRIMARY KEY",
                             "date": "DATE",
                             "description": "NVARCHAR",
                             "amount": "NUMERIC",
                             "categoryId": "INTEGER"
                          })

    CATEGORIES = Table(name="Categories",
                       column_mapping={
                           "categoryId": "INTEGER PRIMARY KEY",
                           "name": "NVARCHAR UNIQUE"
                       })

    VENDORS = Table(name="Vendors",
                    column_mapping={
                        "vendorId": "INTEGER PRIMARY KEY",
                        "vendorMemo": "NVARCHAR UNIQUE",
                        "vendorName": "NVARCHAR"
                    })

    VENDOR_CATEGORIES = Table(name="VendorCategories",
                              column_mapping={
                                  "vendorId": "INTEGER",
                                  "categoryId": "INTEGER",
                                  "count": "INTEGER"
                              },
                              primary_key_column="PRIMARY KEY (vendorId, categoryId)")
