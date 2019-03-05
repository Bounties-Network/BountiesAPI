const {cloneDeep} = require('lodash'),
    {getAsync} = require('./redis_config'),
    {SQS_PARAMS, CONTRACT_VERSION} = require('./constants'),
    {getBlock} = require('./web3_config'),
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
                    _bountyId = '-1',
                },
            } = event, messageParams;

            const messageDeduplicationId = transactionHash + eventName;
            const existingHash = await getAsync(messageDeduplicationId);

            // this means we already synced this hash
            // I do it this way since we keep subscribing to the same block. SQS provides de-duping, but
            // only within shorter timeframes while evaluation is occurring
            if (existingHash) {
                continue;
            }

            bountyId = bountyId === '-1' ? _bountyId : bountyId;

            // console.log({transactionHash});
            // console.log({ "data": event.returnValues, "name": event.event });
            console.log({event});
            const blockData = await getBlock(blockNumber);
            if (!blockData || !('timestamp' in blockData)) {
                highestBlock = blockNumber;
                continue;
            }

            const eventTimestamp = blockData.timestamp.toString();

            // Set Up SQS Params
            messageParams = cloneDeep(SQS_PARAMS);
            messageParams.MessageAttributes.Event.StringValue = event.event;
            messageParams.MessageAttributes.BountyId.StringValue = event.returnValues._bountyId;
            messageParams.MessageAttributes.FulfillmentId.StringValue = fulfillmentId;
            messageParams.MessageAttributes.MessageDeduplicationId.StringValue = messageDeduplicationId;
            messageParams.MessageAttributes.TransactionHash.StringValue = transactionHash;
            messageParams.MessageAttributes.ContractMethodInputs.StringValue = JSON.stringify(sanitizeEventData(event.returnValues));
            messageParams.MessageAttributes.TimeStamp.StringValue = eventTimestamp;
            messageParams.MessageAttributes.TransactionFrom.StringValue = '0x'; //"TODO" ||
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
