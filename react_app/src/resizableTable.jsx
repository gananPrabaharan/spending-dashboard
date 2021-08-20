import ReactDOM from 'react-dom'
import React, { Component } from 'react'
import BootstrapTable from "react-bootstrap-table-next";
import cellEditFactory from "react-bootstrap-table2-editor";
import paginationFactory from "react-bootstrap-table2-paginator";
import filterFactory from "react-bootstrap-table2-filter";
import ColumnResizer from 'column-resizer';


class ResizableTable extends Component {
    constructor(props){
        super(props);
        this.tableId = "somethingUnique";
    }

    componentDidMount() {
        if (this.props.resizable) {
            this.enableResize();
        }
    }

    componentWillUnmount() {
        if (this.props.resizable) {
            this.disableResize();
        }
    }

    componentDidUpdate() {
        if (this.props.resizable) {
            this.enableResize();
        }
    }

    /*
     * In this example, one table controls the resizing of the
     * another table so both tables' columns resize synchronously.
     */
    enableResize = () =>  {
        const options = this.props.resizerOptions;
        if (!this.resizer || true) {
            this.resizer = new ColumnResizer(
                ReactDOM.findDOMNode(this)
                    .querySelector(`#${this.tableId}`), options);
        }
    }

    disableResize = () =>  {
        if (this.resizer) {
            /* This will return the current options object.
             *
             * The options, which include the column widths,
             * can be used to re-create the table with the
             * same column widths as last used.
             */
            this.resizer.reset({ disable: true });
        }
    }

    // Expects three prop values
    // dataList: List of data
    // columns: BootstrapTable columns list
    // changeStateData: Function to change parent dataList property
    afterSaveCell = (oldValue, newValue, row, column) => {
        if (this.props.changeStateData != null){
            if (oldValue !== newValue){
                // Replace the changed row with new row
                for (var i=0; i<this.props.dataList.length; i++){
                    if (this.props.dataList[i].id === row.id){
                        this.props.dataList[i] = row;
                        break;
                    }
                }

                // Reset state with tempData
                this.props.changeStateData(this.props.dataList);
            }
        }
    };
    rowStyle = (row, rowIndex) => {
        if (row === this.props.clickedRow) {
            return {backgroundColor: '#f5f5f5' };
        }
    };

    render(){
        return(
            <div >
                <BootstrapTable
                    id={this.tableId}
                    bootstrap4
                    noDataIndication="No Data Found"
                    condensed
                    // bordered
                    // striped
                    hover
                    loading
                    keyField="id"
                    data={ this.props.dataList }
                    columns={ this.props.columns }
                    pagination={ paginationFactory({}) }
                    cellEdit={ cellEditFactory({mode: "click", blurToSave: true,
                        afterSaveCell:(oldValue, newValue, row, column) => {this.afterSaveCell(oldValue, newValue, row, column)}
                    }) }
                    rowStyle={ this.rowStyle }
                    filter={ filterFactory() }
                />
            </div>
        )
    }

}

export default ResizableTable