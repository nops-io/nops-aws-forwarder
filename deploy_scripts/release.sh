#!/bin/sh

#### setup version
OLD_VERSION=$(cat Release_Version)
OLD_MAIN_VERSION=$(echo $OLD_VERSION | cut -d "." -f 1)
OLD_MAJOR_VERSION=$(echo $OLD_VERSION | cut -d "." -f 2)
OLD_MINOR_VERSION=$(echo $OLD_VERSION | cut -d "." -f 3)

echo "old version ${OLD_VERSION}"

if [ -f $1 ]; then 
    echo "Please provide valid arguments minor, major, main or specific, only specific argument require second argument which is desired version"
    exit 1
elif [ $1 = "minor" ]; then   
    NEW_MINOR_VERSION=`expr $OLD_MINOR_VERSION + 1`
    NEW_VERSION="${OLD_MAIN_VERSION}.${OLD_MAJOR_VERSION}.${NEW_MINOR_VERSION}"
    echo "new version ${NEW_VERSION}"
elif [ $1 = "major" ]; then
    NEW_MAJOR_VERSION=`expr $OLD_MAJOR_VERSION + 1`
    NEW_VERSION="${OLD_MAIN_VERSION}.${NEW_MAJOR_VERSION}.0"
    echo "new version ${NEW_VERSION}"
elif [ $1 = "main" ]; then
    NEW_MAIN_VERSION=`expr $OLD_MAIN_VERSION + 1`
    NEW_VERSION="${NEW_MAIN_VERSION}.0.0"
    echo "new version ${NEW_VERSION}"
elif [ $1 = "specific" ]; then
    NEW_VERSION="${2}"
    echo "new version ${NEW_VERSION}"
fi

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
