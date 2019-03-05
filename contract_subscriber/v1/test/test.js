const assert = require('chai').assert

describe("If ETH_NETWORK is setted in environment", function () {
  it("it should correspond to the established env", function(){
     process.env.eth_network = 'localhost';

     const ETH_NETWORK = require('../constants').ETH_NETWORK;
     assert.equal(ETH_NETWORK, 'localhost');
  });
});
