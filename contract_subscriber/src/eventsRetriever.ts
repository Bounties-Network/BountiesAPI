import { cloneDeep, chain } from "lodash";
import { getAsync } from "./redis_config";
import { CONTRACT_VERSION, SQS_PARAMS } from "./constants";
import { abiDecoder, getTransaction, getBlock } from "./web3_config";
import sqs from "./sqs_config";
import rollbar from "./rollbar";

const camelToUnderscore = (key: string) => {
  return key.replace(/([A-Z])/g, "_$1").toLowerCase();
};

const sanitizeEventData = (obj: any): any => {
  const sanitizedObj = {};
  Object.keys(obj).forEach(key => {
    if (isNaN(Number(key))) {
      // @ts-ignore
      sanitizedObj[camelToUnderscore(key[0] == "_" ? key.substring(1) : key)] = obj[key];
    }
  });

  return sanitizedObj;
};

async function sendEvents(events: any) {
  try {
    let highestBlock;
    for (let event of events) {
      let {
          event: eventName,
          transactionHash,
          blockNumber,
          returnValues: { bountyId = "-1", _fulfillmentId: fulfillmentId = "-1", _bountyId = "-1" }
        } = event,
        messageParams;

      const messageDeduplicationId = transactionHash + eventName;
      const existingHash = await getAsync(messageDeduplicationId);

      // this means we already synced this hash
      // I do it this way since we keep subscribing to the same block. SQS provides de-duping, but
      // only within shorter timeframes while evaluation is ocurring
      if (existingHash) {
        continue;
      }

      bountyId = bountyId === "-1" ? _bountyId : bountyId;

      console.log({ transactionHash });

      let rawTransaction = await getTransaction(transactionHash);

      // retries incase the first call failed
      while (!rawTransaction) {
        console.log("retrying transaction:", transactionHash);
        rawTransaction = await getTransaction(transactionHash);
      }
      const transactionFrom = rawTransaction.from;
      let contractMethodInputs = {};

      if (CONTRACT_VERSION == "v1") {
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
          .keyBy("name")
          .mapValues("value")
          .mapKeys((value, key) => key.substring(1))
          .value();
      }

      let blockData = await getBlock(blockNumber);

      // retries incase the first call failed
      while (!blockData) {
        console.log("retrying blockdata:", blockNumber);
        blockData = await getBlock(blockNumber);
      }

      if (!("timestamp" in blockData)) {
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
      messageParams.MessageAttributes.ContractEventData.StringValue = JSON.stringify(
        sanitizeEventData(event.returnValues)
      );
      messageParams.MessageAttributes.ContractVersion.StringValue = CONTRACT_VERSION;
      messageParams.MessageAttributes.TimeStamp.StringValue = eventTimestamp;
      messageParams.MessageAttributes.TransactionFrom.StringValue = transactionFrom || "0x";
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

export { sendEvents };
