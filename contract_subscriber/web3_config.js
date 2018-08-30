const json = require('./contract.json'),
	  Web3 = require('web3'),
	  abiDecoder = require('abi-decoder'),
	  { ETH_NETWORK, ETH_NETWORK_URL } = require('./constants');

// web3 setup
const web3 = new Web3(ETH_NETWORK_URL);

const StandardBounties = new web3.eth.Contract(
	json.interfaces.StandardBounties,
	json[ETH_NETWORK].standardBountiesAddress
);

abiDecoder.addABI(json.interfaces.StandardBounties);

exports.getBlock = web3.eth.getBlock;
exports.getTransaction = web3.eth.getTransaction;
exports.getBlock = web3.eth.getBlock;
exports.abiDecoder = abiDecoder;
exports.StandardBounties = StandardBounties;
