#!/usr/bin/env node
import 'source-map-support/register';
import cdk = require('@aws-cdk/core');
import { GitopsStack } from '../lib/gitops-stack';

const app = new cdk.App();
new GitopsStack(app, 'GitopsStack');
