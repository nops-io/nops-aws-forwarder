#!/bin/sh
CURRENT_VERSION=$(grep "NOPS_FORWARDER_VERSION" settings.py | awk -v RS='"' '!(NR%2)')
PACKAGE_NAME="nops-aws-forwarder-deployment-package-${CURRENT_VERSION}.zip"
BUNDLE_PATH="./.package/${PACKAGE_NAME}"
gh release create ${PACKAGE_NAME} $BUNDLE_PATH

aws s3 cp deploy_cloudformation/lambda-forwarder-cloudformation-template.yaml s3://nops-cloudformation-template/lambda-forwarder-cloudformation-template-${CURRENT_VERSION}.yaml
aws s3 cp deploy_cloudformation/lambda-forwarder-cloudformation-template.yaml s3://nops-cloudformation-template/lambda-forwarder-cloudformation-template.yaml
