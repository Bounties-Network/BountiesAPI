import React, { Component } from 'react';
import { Form, Select, Button, DatePicker } from 'antd';
import moment from 'moment';

const FormItem = Form.Item;
const { Option } = Select;
const { RangePicker } = DatePicker;
const dateFormat = 'YYYY-MM-DD';

function hasErrors(fieldsError) {
  return Object.keys(fieldsError).some(field => fieldsError[field]);
}

class QueryForm extends Component {
  constructor(props) {
    super(props);
    this.state = {
      range: [
        moment('2018-01-02', dateFormat),
        moment('2018-02-02', dateFormat)
      ],
      schema: 'test'
    };
    this.handleChangeRange = this.handleChangeRange.bind(this);
    this.handleChangeSchema = this.handleChangeSchema.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }
  componentDidMount() {
    this.props.form.validateFields();
  }
  handleChangeRange(value) {
    this.setState({ range: value });
  }
  handleChangeSchema(value) {
    this.setState({ schema: value });
  }
  handleSubmit(e) {
    e.preventDefault();
    this.props.form.validateFields((err) => {
      if (!err) {
        this.props.onQuery(this.state.schema, this.state.range);
      }
    });
  }

  render() {
    const {
      getFieldDecorator,
      getFieldsError,
      getFieldError,
      isFieldTouched
    } = this.props.form;

    const rangeError = isFieldTouched('range') && getFieldError('range');
    const schemaError = isFieldTouched('schema') && getFieldError('schema');
    const schemaOption = (
      <Select
        style={{ width: 120 }}
        onChange={this.handleChangeSchema}
      >
        <Option value="test">test</Option>
        <Option value="all">all</Option>
        <Option value="gitcoin">gitcoin</Option>
      </Select>
    );
    return (
      <Form layout="inline" onSubmit={this.handleSubmit}>
        <FormItem
          validateStatus={rangeError ? 'error' : ''}
          help={rangeError || ''}
        >
          {getFieldDecorator('range', {
            rules: [{ required: true, message: 'Please input date range!' }],
            initialValue: this.state.range
          })(<RangePicker
            onChange={this.handleChangeRange}
            format={dateFormat}
          />)}
        </FormItem>

        <FormItem
          validateStatus={schemaError ? 'error' : ''}
          help={schemaError || ''}
        >
          {getFieldDecorator('schema', {
            rules: [{ required: true, message: 'Please select schema!' }],
            initialValue: this.state.schema
          })(schemaOption)}
        </FormItem>

        <FormItem>
          <Button
            type="primary"
            htmlType="submit"
            disabled={hasErrors(getFieldsError())}
          >
            Query
          </Button>
        </FormItem>
      </Form>
    );
  }
}

const Wrapper = Form.create()(QueryForm);
export default Wrapper;
