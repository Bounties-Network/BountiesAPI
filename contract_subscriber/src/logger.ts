import { createLogger, format, transports } from "winston";
const { combine, timestamp, label, simple } = format;

const logger = createLogger({
  format: combine(label({ label: "contract_subscriber" }), timestamp(), simple()),
  transports: [new transports.Console({ handleExceptions: true })]
});

export default logger;
