#!/bin/sh

#### setup version
OLD_VERSION=$(grep "NOPS_FORWARDER_VERSION" settings.py | awk -v RS='"' '!(NR%2)')
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

#### update files with new release version
sed -i -r "/CTForwarderReleaseVersion/,/Default: [0-9\.]+/s/Default: [0-9\.]+/Default: ${NEW_VERSION}/g" deploy_cloudformation/lambda-forwarder-cloudformation-template.yaml
sed -i -r "s/NOPS_FORWARDER_VERSION = \"[0-9\.]+/NOPS_FORWARDER_VERSION = \"${NEW_VERSION}/g" settings.py

echo "Committing version number change..."
git add settings.py deploy_cloudformation/lambda-forwarder-cloudformation-template.yaml
git commit -m "Bump version from ${OLD_VERSION} to ${NEW_VERSION}"
