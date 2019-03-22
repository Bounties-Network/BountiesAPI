const json = require('./contract.json');
const Web3 = require('web3');
const abiDecoder = require('abi-decoder');
const { CONTRACT_VERSION, ETH_NETWORK, ETH_NETWORK_URL } = require('./constants');


const web3 = new Web3(ETH_NETWORK_URL);

const StandardBounties = new web3.eth.Contract(
	json.version[CONTRACT_VERSION].interfaces.StandardBounties,
	json.version[CONTRACT_VERSION][ETH_NETWORK]
);

abiDecoder.addABI(json.version[CONTRACT_VERSION].interfaces.StandardBounties);

exports.getBlock = web3.eth.getBlock;
exports.getTransaction = web3.eth.getTransaction;
exports.getBlock = web3.eth.getBlock;
exports.abiDecoder = abiDecoder;
exports.StandardBounties = StandardBounties;
