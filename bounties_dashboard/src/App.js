import React, { Component } from 'react';
import { connect } from 'react-redux';
import 'antd/dist/antd.css';
import { Row, Col, Alert, Spin, Card, Layout, Menu, Icon } from 'antd';

import QueryForm from './QueryForm';
import BountyStatesChart from './components/BountyStatesChart';
import LineChart from './components/LineChart';
import BarChart from './components/BarChart';

const { Content, Sider } = Layout;

class App extends Component {
  constructor(props) {
    super(props);
    this.state = { collapsed: false };
    this.onCollapse = this.onCollapse.bind(this);
  }

  onCollapse(collapsed) {
    this.setState({ collapsed });
  }

  render() {
    return (
      <Layout style={{ minHeight: '100vh' }}>
        <Sider
          collapsible
          collapsed={this.state.collapsed}
          onCollapse={this.onCollapse}
        >
          <div className="logo" />
          <Menu theme="dark" defaultSelectedKeys={['1']} mode="inline">
            <Menu.Item key="1">
              <Icon type="pie-chart" />
              <span>Dashboard</span>
            </Menu.Item>
          </Menu>
        </Sider>
        <Layout>
          <Content>
            <Row>
              <Col span={24}>
                <Card bordered={false}>
                  <QueryForm {...this.props} />
                </Card>
              </Col>
            </Row>
            <Spin spinning={this.props.fetching}>
              {this.props.data &&
                <Row>
                  <Col md={8}>
                    {this.props.data.bountyStates &&
                      <BountyStatesChart data={this.props.data.bountyStates} />
                    }
                  </Col>
                  <Col span={16}>
                    {this.props.data.bar &&
                      <BarChart data={this.props.data.bar} />
                    }
                  </Col>
                </Row>}
              {this.props.data &&
                <Row>
                  <Col span={24}>
                    {this.props.data.line &&
                      <LineChart data={this.props.data.line} />
                    }
                  </Col>
                </Row>
              }
              {this.props.error &&
                <Alert
                  message="Something went wrong"
                  description="Fetching data error"
                  type="error"
                />}
            </Spin>
          </Content>
        </Layout>
      </Layout>
    );
  }
}

const mapStateToProps = state => ({
  fetching: state.fetching,
  data: state.data,
  error: state.error
});

const mapDispatchToProps = dispatch => ({
  onQuery: (schema, range) => dispatch({ type: 'API_CALL_REQUEST', schema, range })
});

export default connect(mapStateToProps, mapDispatchToProps)(App);
