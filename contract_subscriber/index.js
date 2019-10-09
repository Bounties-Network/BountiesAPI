"use strict";

const delay = require("delay");
const rollbar = require("./rollbar");
const logger = require("./logger");
const { StandardBounties, getBlock } = require("./web3_config");
const { getAsync, writeAsync } = require("./redis_config");
const { sendEvents } = require("./eventsRetriever");
const { CONTRACT_VERSION } = require("./constants");

async function handler() {
  while (true) {
    try {
      // I use past events vs. subscribe in order to preserve ordering - FIFO
      // Also, subscribe is just polling - the socket connection does not provide the additional behavior, so these
      // are essentially accomplishing the same thing

      // StandardBounties latest events
      let fromBlock = (await getAsync(`currentBlock_${CONTRACT_VERSION}`)) || 0;
      fromBlock = parseInt(fromBlock);
      const latestBlockData = await getBlock("latest");
      const latestBlock = latestBlockData.number;
      // console.log('fromBlock: ', fromBlock);
      // console.log('latestBlock: ', latestBlock)
      let eventBlock;

      while (fromBlock < latestBlock) {
        let events = await StandardBounties.getPastEvents({ fromBlock, toBlock: fromBlock + 100000 });
        logger.info(`currently checking: `, JSON.stringify({ fromBlock, currentBlock, CONTRACT_VERSION }));
        eventBlock = await sendEvents(events);
        if (eventBlock) {
          logger.info("event block: ", JSON.stringify({ eventBlock, fromBlock, currentBlock, CONTRACT_VERSION }));
          break;
        }
        fromBlock += 100000;
      }

      // console.log('eventBlock: ', eventBlock);
      if (eventBlock) {
        await writeAsync(`currentBlock_${CONTRACT_VERSION}`, eventBlock);
      }

      await delay(1000);
    } catch (err) {
      rollbar.error(err);
      logger.info("error occured: ", JSON.stringify({ eventBlock, fromBlock, currentBlock, CONTRACT_VERSION }));
      logger.error("error occured: ", err);
      // console.log(err);
      // ignore constant RPC response error from Infura temporarily
      if (err.message !== 'Invalid JSON RPC response: ""') {
        // exit with error so kubernettes will automatically restart the job
        logger.warn("Invalid JSON RPC response, exiting for pod restart", JSON.stringify(err));
        process.exit(1);
      } else {
        // try again in a little while
        await delay(5000);
      }
    }
  }
}

handler();
