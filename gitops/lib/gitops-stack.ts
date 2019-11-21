import cdk = require('@aws-cdk/core');
import iam = require('@aws-cdk/aws-iam');
import createContainerUser from './container-user'


export class GitopsStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    createContainerUser(this)
  }
}
