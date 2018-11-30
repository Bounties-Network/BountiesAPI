const rollbar = require('./rollbar'),
    { StandardBounties, getBlock } = require('./web3_config'),
    { getAsync, writeAsync } = require('./redis_config'),
    { sendEvents } = require('./eventsRetriever');

exports.readBlock = async (event, context, callback) => {
    try {
        // I use past events vs. subscribe in order to preserve ordering - FIFO
        // Also, subscribe is just polling - the socket connection does not provide the additional behavior, so these
        // are essentially accomplishing the same thing

        // StandardBounties latest events
        let fromBlock = await getAsync('currentBlock') || 0;
        fromBlock = parseInt(fromBlock);
        const latestBlockData = await getBlock('latest');
        const latestBlock = latestBlockData.number;
        let eventBlock;
        while (fromBlock < latestBlock) {
            let events = await StandardBounties.getPastEvents({fromBlock, toBlock: fromBlock + 100000});
            eventBlock = await sendEvents(events);
            if (eventBlock) {
                break;
            }
            fromBlock += 100000;
        }

        if (eventBlock) {
            await writeAsync('currentBlock', eventBlock);
        }
    } catch (err) {
        // ignore constant RPC response error from Infura temporarily
        if (err.message !== 'Invalid JSON RPC response: ""') {
            // include rollbar error message soon
            rollbar.error(err);
            console.log(err);
        }

        throw err;
    }
}
