const SQS_PARAMS = {
  MessageAttributes: {
    Event: {
      DataType: "String",
      StringValue: ""
    },
    BountyId: {
      DataType: "Number",
      StringValue: ""
    },
    FulfillmentId: {
      DataType: "Number",
      StringValue: ""
    },
    MessageDeduplicationId: {
      DataType: "String",
      StringValue: ""
    },
    TransactionHash: {
      DataType: "String",
      StringValue: ""
    },
    ContractMethodInputs: {
      DataType: "String",
      StringValue: ""
    },
    ContractEventData: {
      DataType: "String",
      StringValue: ""
    },
    ContractVersion: {
      DataType: "String",
      StringValue: ""
    },
    TransactionFrom: {
      DataType: "String",
      StringValue: ""
    },
    TimeStamp: {
      DataType: "Number",
      StringValue: ""
    }
  },
  MessageBody: "Event Subscription",
  QueueUrl: process.env["queue_url"] || "https://sqs.us-east-1.amazonaws.com/802922962628/bounties_development.fifo",
  MessageDeduplicationId: "",
  MessageGroupId: "Event_Subscriber"
};

const infuraKey = process.env["infura"];

const networks: { [key: string]: string } = {
  mainNet: "https://mainnet.infura.io/v3/" + infuraKey,
  rinkeby: "https://rinkeby.infura.io/v3/" + infuraKey,
  consensysrinkeby: "https://rinkeby.infura.io/v3/" + infuraKey,
  rinkebystaging: "https://rinkeby.infura.io/v3/" + infuraKey,
  localhost: "localhost:8545"
};

const ethNetwork = process.env["eth_network"] || "mainNet";
const contractVersion = process.env["contract_version"] || "v1";

const ETH_NETWORK: string = ethNetwork;
const ETH_NETWORK_URL: string = networks[ethNetwork];
const CONTRACT_VERSION = contractVersion;

export { CONTRACT_VERSION, ETH_NETWORK_URL, ETH_NETWORK, networks, SQS_PARAMS };
