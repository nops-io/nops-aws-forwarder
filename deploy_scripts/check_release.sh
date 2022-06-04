#!/bin/sh
CURRENT_VERSION=$(grep "NOPS_FORWARDER_VERSION" settings.py | awk -v RS='"' '!(NR%2)')
PACKAGE_NAME="nops-aws-forwarder-deployment-package-${CURRENT_VERSION}.zip"
if gh release list | grep $PACKAGE_NAME; then
    echo "Duplicated release"
    exit 1
fi
