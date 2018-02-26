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
 },
 MessageBody: 'Event Subscription',
 QueueUrl: 'https://sqs.us-east-1.amazonaws.com/802922962628/Bounties.fifo',
 MessageDeduplicationId: '',
 MessageGroupId: 'Event_Subscriber',
};
