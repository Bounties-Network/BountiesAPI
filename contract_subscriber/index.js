'use strict';

const delay = require('delay'),
	  rollbar = require('./rollbar'),
	{ StandardBounties, ETHProfiles } = require('./web3_config'),
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
			let events = await StandardBounties.getPastEvents({fromBlock, toBlock: 'latest'});
			let eventBlock = await sendEvents(events);

			if (eventBlock) {
				await writeAsync('currentBlock', eventBlock);
			}

			// ETHProfiles latest events
			fromBlock = await getAsync('ethProfilesCurrentBlock') || 0;
			events = await ETHProfiles.getPastEvents({fromBlock, toBlock: 'latest'});
			eventBlock = await sendEvents(events);

			if (eventBlock) {
				await writeAsync('ethProfilesCurrentBlock', eventBlock + 1);
			}

			await delay(1000);

		} catch (err) {
			// include rollbar error message soon
			rollbar.error(err);
			console.log(err);

			// exit with error so kubernettes will automatically restart the job
			process.exit(1);
		}
	}
}

handler();
