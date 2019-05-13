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
   'ContractEventData': {
    DataType: 'String',
    StringValue: '',
   },
   'ContractVersion': {
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
 },
 MessageBody: 'Event Subscription',
 QueueUrl: process.env['queue_url'] || 'https://sqs.us-east-1.amazonaws.com/802922962628/bounties_development.fifo',
 MessageDeduplicationId: '',
 MessageGroupId: 'Event_Subscriber',
};

const networks = {
    'mainNet': 'https://mainnet.infura.io/v3/5eb45628ce2c4ecebcce7f201f352792',
    'rinkeby':  'https://rinkeby.infura.io/v3/5eb45628ce2c4ecebcce7f201f352792',
    'consensysrinkeby': 'https://rinkeby.infura.io/v3/5eb45628ce2c4ecebcce7f201f352792',
    'rinkebystaging': 'https://rinkeby.infura.io/v3/5eb45628ce2c4ecebcce7f201f352792',
    'localhost': 'localhost:8545',
}

const ethNetwork = process.env['eth_network'] || 'mainNet';
const contractVersion = process.env['contract_version'] || 'v1';

exports.ETH_NETWORK = ethNetwork;
exports.ETH_NETWORK_URL = networks[ethNetwork];
exports.CONTRACT_VERSION = contractVersion;
