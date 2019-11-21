import { expect as expectCDK, matchTemplate, MatchStyle } from '@aws-cdk/assert';
import cdk = require('@aws-cdk/core');
import Gitops = require('../lib/gitops-stack');

test('Empty Stack', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new Gitops.GitopsStack(app, 'MyTestStack');
    // THEN
    expectCDK(stack).to(matchTemplate({
      "Resources": {}
    }, MatchStyle.EXACT))
});