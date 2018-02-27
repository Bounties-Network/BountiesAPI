const Rollbar = require('rollbar');

const rollbarToken = process.env['rollbar_token'];
const rollbar = new Rollbar({
	enabled: rollbarToken ? true : false,
	accessToken: rollbarToken,
	captureUncaught: true,
	captureUnhandledRejections: true,
});

module.exports = rollbar;
