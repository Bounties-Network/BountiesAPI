'use strict';

const delay = require('delay'),
	  rollbar = require('./rollbar'),
	{ StandardBounties, getBlock } = require('./web3_config'),
	{ getAsync, writeAsync } = require('./redis_config'),
	{ sendEvents } = require('./eventsRetriever');

async function handler() {
	while (true) {
		try {
			// I use past events vs. subscribe in order to preserve ordering - FIFO
			// Also, subscribe is just polling - the socket connection does not provide the additional behavior, so these
			// are essentially accomplishing the same thing

			// StandardBounties latest events
			let fromBlock = await getAsync('currentBlock') || 0;
			fromBlock = parseInt(fromBlock);
			const latestBlockData = await getBlock('latest');
			const latestBlock = latestBlockData.number;
			console.log('fromBlock: ', fromBlock);
			console.log('latestBlock: ', latestBlock)
			let eventBlock;
			while (fromBlock < latestBlock) {
				let events = await StandardBounties.getPastEvents({fromBlock, toBlock: fromBlock + 100000});
				console.log('currentCheck: ', fromBlock);
				eventBlock = await sendEvents(events);
				if (eventBlock) {
					break;
				}
				fromBlock += 100000;
			}

			console.log('eventBlock: ', eventBlock);
			if (eventBlock) {
				await writeAsync('currentBlock', eventBlock);
			}

			await delay(1000);

		} catch (err) {
			// ignore constant RPC response error from Infura temporarily
			if (err.message !== 'Invalid JSON RPC response: ""') {
				// include rollbar error message soon
				rollbar.error(err);
				console.log(err);

				// exit with error so kubernettes will automatically restart the job
				process.exit(1);
			} else {
				// try again in a little while
				await delay(5000);
			}
		}
	}
}

handler();
