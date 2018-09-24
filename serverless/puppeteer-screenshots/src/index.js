const setup = require('./configs/setup');
const axios = require('axios');

exports.handler = async (event, context, callback) => {
  // For keeping the browser launch
  context.callbackWaitsForEmptyEventLoop = false;
  const message = JSON.parse(event.Records[0].Sns.Message);
  const url = message.url;
  const key = message.key;
  if (!url || !key) {
    return callback('Must include url and key in the event');
  }

  const browser = await setup.getBrowser();
  await exports.run(browser, url, key);
  return callback(null, 'success');
};

exports.run = async (browser, url, key) => {
  const page = await browser.newPage();
  await page.goto(url,
   {waitUntil: ['domcontentloaded', 'networkidle0']}
  );
  await page.setViewport({width: 1464, height: 764});
  await page.screenshot({
    path: '/tmp/screenshot.png',
    clip: {
      x: 64,
      y: 64,
      width: 1400,
      height: 700,
    },
  });

  const aws = require('aws-sdk');
  const s3 = new aws.S3({apiVersion: '2006-03-01'});
  const fs = require('fs');
  const screenshot = await new Promise((resolve, reject) => {
    fs.readFile('/tmp/screenshot.png', (err, data) => {
      if (err) return reject(err);
      resolve(data);
    });
  });
  await s3.putObject({
    Bucket: 'assets.bounties.network',
    Key: key,
    Body: screenshot,
    ACL: 'public-read',
  }).promise();
  await page.close();
  await axios.post('https://api.prerender.io/recache', {
    prerenderToken: process.env.PRERENDER_TOKEN,
    url: url,
  });
  return 'done';
};
