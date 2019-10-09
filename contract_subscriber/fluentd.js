var winston = require("winston");
const { format } = require("winston");
const { combine, timestamp, label, prettyPrint } = format;
// var config = {
//   host: "localhost",
//   port: 24224,
//   timeout: 3.0,
//   requireAckResponse: true
// };
// var fluentTransport = require("fluent-logger").support.winstonTransport();
var logger = winston.createLogger({
  format: combine(label({ label: "contract_subscriber" }), timestamp(), prettyPrint()),
  transports: [
    // new fluentTransport("contract_subscriber", config),
    new winston.transports.Console({ handleExceptions: true })
  ]
});

module.exports = logger;
