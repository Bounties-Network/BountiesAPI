import AWS from "aws-sdk";

const myCredentials = new AWS.Credentials("x", "x");

AWS.config.update({ region: "us-east-1" });

const sqs = process.env.local
  ? new AWS.SQS({ credentials: myCredentials, region: "none", endpoint: "http://sqs:9324" })
  : new AWS.SQS();

export default sqs;
