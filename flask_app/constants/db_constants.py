from classes.table import Table


class Tables:
    TRANSACTIONS = Table(name="Transactions",
                         column_mapping={
                             "transactionId": "INTEGER PRIMARY KEY",
                             "date": "DATE",
                             "description": "NVARCHAR",
                             "amount": "NUMERIC",
                             "categoryId": "INTEGER",
                             "vendorId": "INTEGER"
                          })

    CATEGORIES = Table(name="Categories",
                       column_mapping={
                           "categoryId": "INTEGER PRIMARY KEY",
                           "budget": "NUMERIC",
                           "name": "NVARCHAR UNIQUE"
                       })

    VENDORS = Table(name="Vendors",
                    column_mapping={
                        "vendorId": "INTEGER PRIMARY KEY",
                        "vendorName": "NVARCHAR UNIQUE"
                    })

    VENDOR_CATEGORIES = Table(name="VendorCategories",
                              column_mapping={
                                  "vendorId": "INTEGER",
                                  "categoryId": "INTEGER",
                                  "count": "INTEGER"
                              },
                              primary_key_column="PRIMARY KEY (vendorId, categoryId)")


DEFAULT_ID = -1
