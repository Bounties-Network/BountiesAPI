const AWS = require('aws-sdk');

let sqs
if (process.env.local) {
	const myCredentials = new AWS.Credentials('x', 'x');
	sqs = new AWS.SQS({
	    credentials: myCredentials,
	    region: 'none',
	    endpoint: 'http://sqs:9324',
	});
} else {
	AWS.config.update({region: 'us-east-1'});
	sqs = new AWS.SQS();
}

module.exports = sqs;
