const json = require('./contract.json'),
	  Web3 = require('web3');

// web3 setup
const web3 = new Web3('https://mainnet.infura.io');

const StandardBounties = new web3.eth.Contract(
	json.interfaces.StandardBounties,
	json.mainNet.standardBountiesAddress
);

module.exports = StandardBounties;
