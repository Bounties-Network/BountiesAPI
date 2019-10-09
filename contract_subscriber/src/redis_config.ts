import Redis from "ioredis";
import logger from "./logger";

const redis = new Redis(process.env["redis_location"]);
redis.on("error", error => {
  logger.error("Error while trying to connect to Redis", error);
  process.exit(1);
});

redis.on("connect", () => {
  logger.info("Redis connected to: ", process.env["redis_location"]);
});

export default redis;
