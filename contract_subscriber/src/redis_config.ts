import redis from "redis";
import { promisify } from "util";

const client = redis.createClient({ url: process.env["redis_location"] });

const getAsync = promisify(client.get).bind(client);

const writeAsync = promisify(client.set).bind(client);

export { getAsync, writeAsync };
