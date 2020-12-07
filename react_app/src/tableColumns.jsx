import {Type} from "react-bootstrap-table2-editor";

export const createActionFormat = (actionFunction, buttonName) => {
    return (cell, row) => {
        return (
            <div>
                <button type="button" className="btn btn-outline-danger btn-sm ml-2 ts-buttom" size="sm"
                    onClick={() => {actionFunction(row)}}>
                    {buttonName}
                </button>
            </div>
        );
    }
}

export const getTransactionTableColumns = (categoryList) => {
    const transactionTableColumns = [
        {
            dataField: "id",
            text: "Transaction Id",
            headerAlign: "center",
            editable: false,
            hidden: true,
            headerStyle: (column, colIndex) => {
              return { width: '5%', textAlign: 'center' };
            }
        },
        {
            dataField: "date",
            text: "Date",
            headerAlign: "center",
            editable: false,
            sort: true,
            headerStyle: (column, colIndex) => {
              return { width: '10%', textAlign: 'center' };
            }
        },
        {
            dataField: "description",
            text: "Description",
            headerAlign: "center",
            editable: false,
            sort: true,
            headerStyle: (column, colIndex) => {
              return { width: '30%', textAlign: 'center' };
            }
        },
        {
            dataField: "withdrawal",
            text: "Withdrawal",
            type: "string",
            headerAlign: "center",
            editable: false,
            sort: true,
            headerStyle: (column, colIndex) => {
              return { width: '10%', textAlign: 'center' };
            }
        },
        {
            dataField: "deposit",
            text: "Deposit",
            type: "string",
            headerAlign: "center",
            editable: false,
            sort: true,
            headerStyle: (column, colIndex) => {
              return { width: '10%', textAlign: 'center' };
            }
        },
        {
            dataField: "category",
            text: "Category",
            type: "string",
            headerAlign: "center",
            editable: true,
            editor: {
                type: Type.SELECT,
                options: categoryList.map(item => {return({value: item, label: item})})
            },
            sort: true,
            headerStyle: (column, colIndex) => {
              return { width: '10%', textAlign: 'center' };
            }
        }
    ];
    return transactionTableColumns
}

export const getCategoriesTableColumns = (actionFunction) => {
    const actionFormat = createActionFormat(actionFunction, "Delete")
    const categoriesTableColumns = [
        {
            dataField: "id",
            text: "Category Id",
            headerAlign: "center",
            editable: false,
            hidden: true,
        },
        {
            dataField: "name",
            text: "Category Name",
            headerAlign: "center",
            editable: false,
            sort: true,
            headerStyle: (column, colIndex) => {
              return { width: '80%', textAlign: 'center' };
            }
        },
        {
            text: "Action",
            dataField: "",
            headerAlign: "center",
            editable: false,
            formatter: actionFormat,
            headerStyle: (column, colIndex) => {
              return { width: '20%', textAlign: 'center' };
            }

        }
    ];
    return categoriesTableColumns
}