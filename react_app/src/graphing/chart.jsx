import React from "react";
import { Bar } from 'react-chartjs-2';

const BarChart = (props) => {
    const data = {
        labels: props.labels,
        datasets: props.datasets,
    };
      
    const options = {
        scales: {
          xAxes: [{
            "stacked": true
          }],
          yAxes: [
            {
              ticks: {
                beginAtZero: true,
              },
            },
          ],
        },
    };
    return (
        <Bar data={data} options={options} />
    )
}

export default BarChart