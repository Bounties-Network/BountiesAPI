
import React from 'react';
import Highcharts from 'highcharts';

function getSeriesObject(data) {
  return [{
    name: 'bounties issued',
    data: data.bountiesIssued
  }, {
    name: 'fulfillments submitted',
    data: data.fulfillmentsSubmitted
  }, {
    name: 'fulfillments accepted',
    data: data.fulfillmentsAccepted
  }, {
    name: 'fulfillments pending acceptance',
    data: data.fulfillmentsPendingAcceptance
  }];
}

class LineChart extends React.Component {
  // When the DOM is ready, create the chart.
  componentDidMount() {
    this.chart = Highcharts.chart('line-chart', {
      title: {
        text: 'Line Chart'
      },
      legend: {
        layout: 'horizontal',
        align: 'center',
        verticalAlign: 'bottom'
      },

      plotOptions: {
        series: {
          label: {
            connectorAllowed: false
          },
          pointStart: 2018
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
    return <div id="line-chart" />;
  }
}

export default LineChart;
