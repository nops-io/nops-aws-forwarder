#!/bin/sh
CURRENT_VERSION=$(grep "NOPS_FORWARDER_VERSION" settings.py | awk -v RS='"' '!(NR%2)')
PACKAGE_NAME="nops-aws-forwarder-deployment-package-${CURRENT_VERSION}.zip"
BUNDLE_PATH="./.package/${PACKAGE_NAME}"
go get github.com/github/hub
hub release create -a $BUNDLE_PATH -m "${PACKAGE_NAME}" ${PACKAGE_NAME} 
