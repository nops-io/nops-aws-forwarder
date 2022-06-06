#!/bin/sh
OLD_VERSION=$(grep "NOPS_FORWARDER_VERSION" settings.py | awk -v RS='"' '!(NR%2)')
NEW_VERSION=$(cat Release_Version)
PACKAGE_NAME="nops-aws-forwarder-deployment-package-${NEW_VERSION}.zip"
BUNDLE_PATH="./.package/${PACKAGE_NAME}"

#### update files with new release version
sed -i -r "s/${OLD_VERSION}/${NEW_VERSION}/g" deploy_cloudformation/lambda-forwarder-cloudformation-template.yaml
sed -i -r "s/${OLD_VERSION}/${NEW_VERSION}/g" Release_Version

#### create github release
gh release create ${PACKAGE_NAME} $BUNDLE_PATH

# #### upload new release cloudformation templates to s3 bucket
aws s3 cp deploy_cloudformation/lambda-forwarder-cloudformation-template.yaml s3://nops-cloudformation-template/lambda-forwarder-cloudformation-template-${NEW_VERSION}.yaml
aws s3 cp deploy_cloudformation/lambda-forwarder-cloudformation-template.yaml s3://nops-cloudformation-template/lambda-forwarder-cloudformation-template.yaml
