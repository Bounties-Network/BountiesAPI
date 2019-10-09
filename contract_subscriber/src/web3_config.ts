import json from "./contract";
import Web3 from "web3";
import abiDecoder from "abi-decoder";
import { CONTRACT_VERSION, ETH_NETWORK, ETH_NETWORK_URL } from "./constants";

const web3 = new Web3(ETH_NETWORK_URL);

const StandardBounties = new web3.eth.Contract(
  json.version[CONTRACT_VERSION].interfaces.StandardBounties,
  json.version[CONTRACT_VERSION][ETH_NETWORK]
);

abiDecoder.addABI(json.version[CONTRACT_VERSION].interfaces.StandardBounties);

const getBlock = web3.eth.getBlock;
const getTransaction = web3.eth.getTransaction;

export { getBlock, getTransaction, StandardBounties, abiDecoder };
