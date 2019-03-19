exports.SQS_PARAMS = {
 MessageAttributes: {
  'Event': {
    DataType: 'String',
    StringValue: '',
   },
   'BountyId': {
    DataType: 'Number',
    StringValue: '',
   },
   'FulfillmentId': {
   	DataType: 'Number',
   	StringValue: '',
   },
   'MessageDeduplicationId': {
    DataType: 'String',
    StringValue: '',
   },
   'TransactionHash': {
    DataType: 'String',
    StringValue: '',
   },
   'ContractMethodInputs': {
    DataType: 'String',
    StringValue: '',
   },
   'TransactionFrom': {
    DataType: 'String',
    StringValue: '',
   },
   'TimeStamp': {
    DataType: 'Number',
    StringValue: '',
   },
   'ContractVersion': {
    DataType: 'Number',
    StringValue: '',
   },
 },
 MessageBody: 'Event Subscription',
 QueueUrl: process.env['queue_url'] || 'https://sqs.us-east-1.amazonaws.com/802922962628/bounties_development.fifo',
 MessageDeduplicationId: '',
 MessageGroupId: 'Event_Subscriber',
};

const networks = {
    'mainNet': 'https://mainnet.infura.io/',
    'rinkeby':  'https://rinkeby.infura.io/',
    'rinkeby-dev': 'https://rinkeby.infura.io',
    'consensysrinkeby': 'https://rinkeby.infura.io/',
    'rinkebystaging': 'https://rinkeby.infura.io/',
    'localhost': 'localhost:8545',
}

const ethNetwork = process.env['eth_network'] || 'mainNet';

exports.ETH_NETWORK = ethNetwork;
exports.ETH_NETWORK_URL = networks[ethNetwork];
