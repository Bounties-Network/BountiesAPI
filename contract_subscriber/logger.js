const { createLogger, format, transports } = require("winston");
const { combine, timestamp, label, prettyPrint } = format;

const logger = createLogger({
  format: combine(label({ label: "contract_subscriber" }), timestamp(), prettyPrint()),
  transports: [new transports.Console({ handleExceptions: true })]
});

module.exports = logger;
