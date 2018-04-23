
import React from 'react';
import Highcharts from 'highcharts';

function getSeriesObject(data) {
  return [{
    name: 'bounty fulfilled rate',
    data: data.bountyFulfilledRate
  }, {
    name: 'avg fulfiller acceptance rate',
    data: data.avgFulfillerAcceptanceRate
  }, {
    name: 'avg fulfillment amount',
    data: data.avgFulfillmentAmount
  }];
}

class BarChart extends React.Component {
  // When the DOM is ready, create the chart.
  componentDidMount() {
    this.chart = Highcharts.chart('bar-chart', {
      chart: {
        type: 'column'
      },
      title: {
        text: 'Rate Bar Chart'
      },
      legend: {
        layout: 'horizontal',
        align: 'center',
        verticalAlign: 'bottom'
      },
      plotOptions: {
        column: {
          stacking: 'normal'
        }
      },
      xAxis: {
        type: 'datetime',
        dateTimeLabelFormats: {
          day: '%d %b'
        }
      },
      series: getSeriesObject(this.props.data),
      responsive: {
        rules: [{
          condition: {
            maxWidth: 500
          },
          chartOptions: {
            legend: {
              layout: 'horizontal',
              align: 'center',
              verticalAlign: 'bottom'
            }
          }
        }]
      }
    });
    setTimeout(() => {
      this.chart.reflow();
    }, 0);
  }
  componentWillReceiveProps(nextProps) {
    if (nextProps.data !== this.props.data) {
      this.chart.update({ series: getSeriesObject(nextProps.data) }, true);
    }
  }
  componentWillUnmount() {
    this.chart.destroy();
  }

  render() {
    return <div id="bar-chart" />;
  }
}

export default BarChart;
