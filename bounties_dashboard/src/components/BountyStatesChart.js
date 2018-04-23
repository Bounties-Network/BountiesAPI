
import React from 'react';
import Highcharts from 'highcharts';

function getDataObject(data) {
  return [{
    name: 'draft',
    y: data[0]
  }, {
    name: 'active',
    y: data[1]
  }, {
    name: 'completed',
    y: data[2]
  }, {
    name: 'expired',
    y: data[3]
  }, {
    name: 'dead',
    y: data[4]
  }];
}

class BountyStatesChart extends React.Component {
  // When the DOM is ready, create the chart.
  componentDidMount() {
    this.chart = Highcharts.chart('bounty-states-chart', {
      chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie'
      },
      title: {
        text: 'Bounty states'
      },
      tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
      },
      plotOptions: {
        pie: {
          allowPointSelect: true,
          cursor: 'pointer',
          dataLabels: {
            enabled: false
          },
          showInLegend: true
        }
      },
      series: [{
        name: 'Bounty Status',
        colorByPoint: true,
        data: getDataObject(this.props.data)
      }]
    });
    setTimeout(() => {
      this.chart.reflow();
    }, 0);
  }
  componentWillReceiveProps(nextProps) {
    if (nextProps.data !== this.props.data) {
      this.chart.series[0].update({
        data: getDataObject(nextProps.data)
      }, true);
    }
  }
  componentWillUnmount() {
    this.chart.destroy();
  }

  render() {
    return <div id="bounty-states-chart" />;
  }
}

export default BountyStatesChart;
