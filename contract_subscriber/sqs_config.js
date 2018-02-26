const AWS = require('aws-sdk');

AWS.config.update({region: 'us-east-1'});
const sqs = new AWS.SQS();

module.exports = sqs;
