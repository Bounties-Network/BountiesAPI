const { cloneDeep, chain } = require('lodash');
const { getAsync } = require('./redis_config');
const { CONTRACT_VERSION, SQS_PARAMS } = require('./constants');
const { abiDecoder, getTransaction, getBlock } = require('./web3_config');
const sqs = require('./sqs_config');
const rollbar = require('./rollbar');


camelToUnderscore= (key) => {
    return key.replace( /([A-Z])/g, "_$1").toLowerCase();
}

sanitizeEventData = (obj) => {
    const sanitizedObj = {};
    Object.keys(obj).forEach(key => {
        if (key.match(/_.+/g)) {
            sanitizedObj[camelToUnderscore(key.substring(1))] = obj[key];
        }
    });

    return sanitizedObj;
};

async function sendEvents(events) {
	try {
		let highestBlock;
		for (let event of events) {
			let {
				event: eventName,
				transactionHash,
				blockNumber,
				returnValues: {
					bountyId = '-1',
					_fulfillmentId: fulfillmentId = '-1',
					_bountyId ='-1',
				},
			} = event, messageParams;

			const messageDeduplicationId = transactionHash + eventName;
			const existingHash = await getAsync(messageDeduplicationId);

			// this means we already synced this hash
			// I do it this way since we keep subscribing to the same block. SQS provides de-duping, but
			// only within shorter timeframes while evaluation is ocurring
			if (existingHash) {
				continue;
			}

			bountyId = bountyId === '-1' ? _bountyId : bountyId;

			console.log({ transactionHash });

			const rawTransaction = await getTransaction(transactionHash);
			const transactionFrom = rawTransaction.from;
			let contractMethodInputs = {};	

			if (CONTRACT_VERSION == 'v1') {
				const rawContractMethodInputs = abiDecoder.decodeMethod(rawTransaction.input);

				// if the bounty contract is called as an internal transaction, it will fail here
				// because we use the tx input to populate our database. In the case of internal
				// transactions, that tx input is the original input to a smart contract wallet
				// or whatever contract made the internal call to bounties
				if (!rawContractMethodInputs) {
					rollbar.error(`Unable to decode transaction input using ABI: ${transactionHash}`);
					continue;
				}

				contractMethodInputs = chain(rawContractMethodInputs.params)
					.keyBy('name')
					.mapValues('value')
					.mapKeys((value, key) => key.substring(1))
					.value();
			}

			const blockData = await getBlock(blockNumber);
			if (!('timestamp' in blockData)) {
				highestBlock = blockNumber;
				continue;
			}

			const eventTimestamp = blockData.timestamp.toString();

			// Set Up SQS Params
			messageParams = cloneDeep(SQS_PARAMS);
			messageParams.MessageAttributes.Event.StringValue = eventName;
			messageParams.MessageAttributes.BountyId.StringValue = bountyId;
			messageParams.MessageAttributes.FulfillmentId.StringValue = fulfillmentId;
			messageParams.MessageAttributes.MessageDeduplicationId.StringValue = messageDeduplicationId;
			messageParams.MessageAttributes.TransactionHash.StringValue = transactionHash;
			messageParams.MessageAttributes.ContractMethodInputs.StringValue = JSON.stringify(contractMethodInputs);
			messageParams.MessageAttributes.ContractEventData.StringValue = JSON.stringify(sanitizeEventData(event.returnValues))
			messageParams.MessageAttributes.ContractVersion.StringValue = CONTRACT_VERSION;
			messageParams.MessageAttributes.TimeStamp.StringValue = eventTimestamp;
			messageParams.MessageAttributes.TransactionFrom.StringValue = transactionFrom || '0x';
			messageParams.MessageDeduplicationId = messageDeduplicationId;

			await sqs.sendMessage(messageParams).promise();
			highestBlock = blockNumber;
		}

		return highestBlock;
	} catch (error) {
		// let index handle and log the error
		throw error;
	}
}

module.exports.sendEvents = sendEvents;
