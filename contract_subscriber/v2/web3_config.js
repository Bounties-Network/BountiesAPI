const json = require('./contract.json'),
	  Web3 = require('web3'),
	  abiDecoder = require('abi-decoder'),
	  { ETH_NETWORK, ETH_NETWORK_URL } = require('./constants');

// web3 setup
const web3 = new Web3(ETH_NETWORK_URL);

const StandardBounties = new web3.eth.Contract(
	json.interfaces.StandardBounty,
	json[ETH_NETWORK].standardBountiesAddress
);

abiDecoder.addABI(json.interfaces.StandardBounty);

exports.getBlock = web3.eth.getBlock;
exports.subscribe = web3.eth.subscribe;
exports.getTransaction = web3.eth.getTransaction;
exports.abiDecoder = abiDecoder;
exports.StandardBounties = StandardBounties;
