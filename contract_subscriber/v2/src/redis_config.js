const redis = require('redis'),
	{ promisify } = require('util');

const client = redis.createClient({ 
	url: `redis://${process.env['redis_host']}:${process.env['redis_port']}`
});

exports.getAsync = promisify(client.get).bind(client);
exports.writeAsync = promisify(client.set).bind(client);
