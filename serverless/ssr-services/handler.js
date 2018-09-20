const aws = require('aws-sdk');
const s3 = new aws.S3({apiVersion: '2006-03-01'});
const axios = require('axios');

exports.uploadSitemap = async (event, context, callback) => {
  const url = event.url;
  const bucket = event.bucket;

  if (url && bucket) {
    callback(null, 'success');
  } else {
    callback('Url and Bucket required in the event');
  }

  const request = await axios.get(url);
  await s3.putObject({
    Bucket: bucket,
    Key: 'sitemap.xml',
    Body: request.data,
    ACL: 'public-read',
    // no cache so we do not have to invalidate cloudfront
    CacheControl: 'no-cache',
  }).promise();
};

exports.setCache = async (event, context, callback) => {
  const url = event.url;
  if (url) {
    callback(null, 'success');
  } else {
    callback('Must pass a url to the event');
  }

  await axios.post('https://api.prerender.io/recache', {
    prerenderToken: process.env.PRERENDER_TOKEN,
    url: url,
  });
}
