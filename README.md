# Aws Nops Forwarder

Forward event from AWS CT into nOps

## Prerequisites
- [AWS Cloudtrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-create-a-trail-using-the-console-first-time.html) with s3 bucket for cloudtrail logs must be configured before deploying this stack. 
- Region for AWS Cloudtrail and nOps-aws-forwarder should be same.

## Installation

### CloudFormation
[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home#/stacks/create/review?stackName=nops-aws-forwarder&templateURL=https://nops-cloudformation-template.s3.us-west-2.amazonaws.com/lambda-forwarder-cloudformation-template.yaml)

1. Log into your admin AWS account/role and deploy the CloudFormation Stack with the button above.
2. Fill in `pnOpsApiKey`, `pCTForwarderReleaseVersion`, `pCloudtrailBucketName`, . All other parameters are optional.
3. Click **Create stack**, and wait for the creation to complete.
4. Find the installed forwarder Lambda function under the stack's "Resources" tab with logical ID `rLambdaForwarder`.
5. Set up [triggers](https://docs.aws.amazon.com/lambda/latest/dg/with-cloudtrail-example.html) to the installed Forwarder
6. Repeat the above steps in another region if you operate in multiple AWS regions with single-region trail.


### Manual
If you can't install the Forwarder using the provided CloudFormation template, you can install the Forwarder manually following the steps below. Feel free to open an issue or pull request to let us know if there is anything we can improve to make the template work for you.

1. Create a Python 3.9 Lambda function using `nops-aws-forwarder-deployment-package-<VERSION>.zip` from the latest [releases](https://github.com/nops-io/nops-aws-forwarder/releases).
2. Save your [NOPS API key](https://app.nops.io/v3/settings?tab=API%20Key) to Lambda's environment variable `NOPS_API_KEY`.
3. Add the `s3:GetObject` permission to the Lambda execution role.
4. Configure [triggers](https://docs.aws.amazon.com/lambda/latest/dg/with-cloudtrail-example.html).

## Upgrade

## Usage

## Support


## Development
- Run ./bump_version minor/major/main to add a new version
