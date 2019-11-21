import cdk = require('@aws-cdk/core');
import iam = require('@aws-cdk/aws-iam');
import { ManagedPolicy } from '@aws-cdk/aws-iam';

const resourcePolicies = [
  'AmazonSQSFullAccess',
  'AmazonSESFullAccess',
  'AmazonSNSFullAccess'
]

export default (scope: cdk.Construct) => {
  const user = new iam.User(scope, "containerUser")

    resourcePolicies.map(policy => user.addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policy)))
    const accessKey = new iam.CfnAccessKey(scope, 'containerUserAccessKey', {
      userName: user.userName,
    });

    new cdk.CfnOutput(scope, 'containerUserAccessKeyId', { value: accessKey.ref });
    new cdk.CfnOutput(scope, 'containerUserSecretAccessKey', { value: accessKey.attrSecretAccessKey });

}