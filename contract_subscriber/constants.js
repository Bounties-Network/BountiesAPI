exports.SQS_PARAMS = {
 MessageAttributes: {
  'Event': {
    DataType: 'String',
    StringValue: ''
   },
   'BountyId': {
    DataType: 'Number',
    StringValue: ''
   },
   'FulfillmentId': {
   	DataType: 'Number',
   	StringValue: '',
   },
   'TransactionHash': {
    DataType: 'String',
    StringValue: '',
   },
 },
 MessageBody: 'Event Subscription',
 QueueUrl: process.env['queue_url'] || 'https://sqs.us-east-1.amazonaws.com/802922962628/bounties_development.fifo',
 MessageDeduplicationId: '',
 MessageGroupId: 'Event_Subscriber',
};
