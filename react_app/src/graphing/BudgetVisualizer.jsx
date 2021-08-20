import { useState, useEffect } from 'react'
import BarChart from './Chart.jsx'

const BudgetVisualizer = (props) => {
    const [chartState, setChartState] = useState({
        labels: [],
        datasets: []
    });

    useEffect( ()=>{categorySpending() }, [props]);

    const categorySpending = () => {
        let categoryLabels = [];
        let datasets = [];
        if (props.categoryDict != null && props.transactions != null){
            // Create items array
            const categorySpending = {};
            const catIds = Object.keys(props.categoryDict).sort();
            const budgets = [];
            for (var i=0; i<catIds.length; i++){
                const currCatDict = props.categoryDict[catIds[i]];
                const catName = currCatDict["name"];
                if (catName.length > 0){
                    categoryLabels.push(catName);
                    budgets.push(currCatDict["budget"]);
                }
            }
            
            // Create dictionary mapping category name to amount spent in transactions
            categoryLabels.map((label) => {categorySpending[label] = 0})
            for (var i=0; i<props.transactions.length; i++){
                const trans = props.transactions[i];
                const catName = props.categoryDict[trans.categoryId]["name"];
                if (catName in categorySpending){
                    categorySpending[catName] -= trans.amount.toFixed(2);
                }
            }

            // Assemble dictionary to create chart from
            const spending = categoryLabels.map((name)=>{return categorySpending[name].toFixed(2)});
            const spendingColors = categoryLabels.map((x) => {return 'rgba(255, 99, 132, 0.2)'} )
            const budgetColors = budgets.map((x) => {return 'rgba(75, 192, 192, 0.2)'} )
            datasets = [
                {"data": spending, "label": "Spending", backgroundColor: spendingColors},
                {"label": "Budget", "data": budgets, backgroundColor: budgetColors, 'fill': true}
            ];
            setChartState({...chartState, labels: categoryLabels, datasets: datasets});
        }
    }

    return (
        <BarChart labels={chartState.labels} datasets={chartState.datasets}></BarChart>
    )
}

export default BudgetVisualizer;