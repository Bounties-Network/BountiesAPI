import React, { Component } from 'react';
import { connect } from 'react-redux';
import 'antd/dist/antd.css';
import { Alert, Spin, Card, Layout, Menu, Icon } from 'antd';

import QueryForm from './QueryForm';

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
          <Content style={{ padding: '30px' }}>
            <Card title="Query" style={{ marginBottom: '30px' }}>
              <QueryForm {...this.props} />
            </Card>
            <Spin spinning={this.props.fetching}>
              {this.props.data &&
                <Alert
                  message="Data"
                  description={JSON.stringify(this.props.data)}
                  type="info"
                />}
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
