const redis = require('redis'),
	{ promisify } = require('util');

const client = redis.createClient();
exports.getAsync = promisify(client.get).bind(client);
exports.writeAsync = promisify(client.set).bind(client);
