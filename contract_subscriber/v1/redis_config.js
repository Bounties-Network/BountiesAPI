const redis = require('redis'),
	{ promisify } = require('util');

const client = redis.createClient({ url: process.env['redis_location'] });

exports.getAsync = promisify(client.get).bind(client);
exports.writeAsync = promisify(client.set).bind(client);
