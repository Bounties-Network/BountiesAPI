const { cloneDeep, chain } = require('lodash'),
	  { getAsync } = require('./redis_config'),
	  { SQS_PARAMS } = require('./constants'),
	  { abiDecoder, getTransaction, getBlock } = require('./web3_config'),
		sqs = require('./sqs_config'),
		rollbar = require('./rollbar');


sanitizeEventData = (obj) => {
    const sanitizedObj = {};
    Object.keys(obj).forEach(key => {
        if (key.match(/_.+/g)) {
            sanitizedObj[key.substring(1)] = obj[key];
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
			const rawContractMethodInputs = abiDecoder.decodeMethod(rawTransaction.input);

			const blockData = await getBlock(blockNumber);

			if (!('timestamp' in blockData)) {
				highestBlock = blockNumber;
				continue;
			}

			const eventTimestamp = blockData.timestamp.toString();

			bountyId = event.returnValues._bountyId;

			// Set Up SQS Params
			messageParams = cloneDeep(SQS_PARAMS);
			messageParams.MessageAttributes.Event.StringValue = eventName;
			messageParams.MessageAttributes.BountyId.StringValue = bountyId;
			messageParams.MessageAttributes.FulfillmentId.StringValue = fulfillmentId;
			messageParams.MessageAttributes.MessageDeduplicationId.StringValue = messageDeduplicationId;
			messageParams.MessageAttributes.TransactionHash.StringValue = transactionHash;
			messageParams.MessageAttributes.ContractMethodInputs.StringValue = JSON.stringify(sanitizeEventData(event.returnValues));
			messageParams.MessageAttributes.TimeStamp.StringValue = eventTimestamp;
			messageParams.MessageAttributes.TransactionFrom.StringValue = transactionFrom || '0x';
			messageParams.MessageAttributes.ContractVersion.StringValue = '2';
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
