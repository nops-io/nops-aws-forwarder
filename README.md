# Aws Nops Forwarder

Forward event from AWS CT into nOps

## Installation


### CloudFormation

[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home#/stacks/create/review?stackName=datadog-forwarder&templateURL=https://github.com/nops-io/nops-aws-forwarder/raw/deploy/cf_deploy/lambda-forwarder-cloudformation-template.yaml)

1. Log into your admin AWS account/role and deploy the CloudFormation Stack with the button above.
2. Fill in `pnOpsApiKey`, `pLambdaPackageS3BucketName`, `pLambdaPackageFileName`, `pCloudtrailBucketName`, . All other parameters are optional.
3. Click **Create stack**, and wait for the creation to complete.
4. Find the installed forwarder Lambda function under the stack's "Resources" tab with logical ID `Forwarder`.
5. Set up triggers to the installed Forwarder
6. Repeat the above steps in another region if you operate in multiple AWS regions.


### Manual
If you can't install the Forwarder using the provided CloudFormation template, you can install the Forwarder manually following the steps below. Feel free to open an issue or pull request to let us know if there is anything we can improve to make the template work for you.

1. Create a Python 3.9 Lambda function using `nops-aws-forwarder-deployment-package-<VERSION>.zip` from the latest [releases](https://github.com/nops-io/nops-aws-forwarder/releases).
2. Save your [NOPS API key](https://app.nops.io/v3/settings?tab=API%20Key) to Lambda's environment variable `NOPS_API_KEY`.
3. Add the `s3:GetObject` permission to the Lambda execution role.
4. Configure [triggers]().


## Usage

## Support
