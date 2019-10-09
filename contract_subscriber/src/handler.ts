import delay from "delay";
import rollbar from "./rollbar";
import logger from "./logger";
import { StandardBounties, getBlock } from "./web3_config";
import redis from "./redis_config";
import { sendEvents } from "./eventsRetriever";
import { CONTRACT_VERSION } from "./constants";

export default async function handler() {
  logger.info("Executing code inside contract_subscriber handler");
  while (true) {
    try {
      // I use past events vs. subscribe in order to preserve ordering - FIFO
      // Also, subscribe is just polling - the socket connection does not provide the additional behavior, so these
      // are essentially accomplishing the same thing

      // StandardBounties latest events
      const currentStoredBlock = await redis.get(`currentBlock_${CONTRACT_VERSION}`);
      // logger.info("Current stored block", { currentStoredBlock });
      let fromBlock = parseInt(currentStoredBlock || "0");
      const latestStoredBlockData = await getBlock("latest");
      const latestBlock = latestStoredBlockData.number;
      logger.info("Current and Latest stored blocks: ", { latestBlock, currentStoredBlock });
      let eventBlock;

      while (fromBlock < latestBlock) {
        let events = await StandardBounties.getPastEvents("allEvents", { fromBlock, toBlock: fromBlock + 100000 });
        logger.info(`Currently checking`, { fromBlock, latestBlock, CONTRACT_VERSION });
        eventBlock = await sendEvents(events);
        if (eventBlock) {
          break;
        }
        fromBlock += 100000;
      }

      if (eventBlock) {
        logger.info("Event block written: ", { eventBlock, fromBlock, latestBlock, CONTRACT_VERSION });
        await redis.set(`currentBlock_${CONTRACT_VERSION}`, eventBlock);
      }

      await delay(1000);
    } catch (err) {
      rollbar.error(err);
      // ignore constant RPC response error from Infura temporarily
      logger.error("Error occured: ", err);
      if (err.message !== 'Invalid JSON RPC response: ""') {
        // exit with error so kubernettes will automatically restart the job
        logger.warn("Invalid JSON RPC response, exiting for pod restart", err);
        process.exit(1);
      } else {
        // try again in a little while
        await delay(5000);
      }
    }
  }
}
