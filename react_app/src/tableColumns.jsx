export const transactionTableColumns = [
    {
        dataField: "id",
        text: "Transaction Id",
        headerAlign: "center",
        editable: false,
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
          return { width: '10%', textAlign: 'center' };
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
          return { width: '30%', textAlign: 'center' };
        }
    }
];
