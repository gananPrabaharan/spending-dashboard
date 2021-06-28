from classes.table import Table


class Tables:
    USERS = Table(name="Users",
                  column_mapping={
                      "userId": "INTEGER PRIMARY KEY",
                      "userUid": "NVARCHAR UNIQUE"
                  })

    TRANSACTIONS = Table(name="Transactions",
                         column_mapping={
                             "transactionId": "INTEGER PRIMARY KEY",
                             "userId": "INTEGER",
                             "date": "DATE",
                             "description": "NVARCHAR",
                             "amount": "NUMERIC",
                             "categoryId": "INTEGER",
                             "vendorId": "INTEGER"
                          })

    CATEGORIES = Table(name="Categories",
                       column_mapping={
                            "categoryId": "INTEGER PRIMARY KEY",
                            "userId": "INTEGER",
                            "budget": "NUMERIC",
                            "name": "NVARCHAR UNIQUE"
                       })

    VENDORS = Table(name="Vendors",
                    column_mapping={
                        "vendorId": "INTEGER PRIMARY KEY",
                        "userId": "INTEGER",
                        "vendorName": "NVARCHAR UNIQUE"
                    })

    VENDOR_CATEGORIES = Table(name="VendorCategories",
                              column_mapping={
                                  "vendorId": "INTEGER",
                                  "userId": "INTEGER",
                                  "categoryId": "INTEGER",
                                  "count": "INTEGER"
                              },
                              primary_key_column="PRIMARY KEY (vendorId, categoryId)")
