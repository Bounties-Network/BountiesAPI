const json = require('./contract.json'),
	  Web3 = require('web3'),
	  { ETH_NETWORK, ETH_NETWORK_URL } = require('./constants');

// web3 setup
const web3 = new Web3(ETH_NETWORK_URL);

const StandardBounties = new web3.eth.Contract(
	json.interfaces.StandardBounties,
	json[ETH_NETWORK].standardBountiesAddress
);

module.exports = StandardBounties;
