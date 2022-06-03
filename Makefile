CURRENT_VERSION := $(shell grep NOPS_FORWARDER_VERSION settings.py | awk -v RS='\"' '!(NR%2)')
PACKAGE_NAME := "nops-aws-forwarder-deployment-package-$(CURRENT_VERSION).zip"

package:
	mkdir -p ./.package/
	rm -rf venv
	python3 -m venv venv
	. venv/bin/activate; pip install -r requirements.txt
	cd venv/lib/python/site-packages; zip -r ../../../../.package/nops-aws-forwarder-deployment-package-$(CURRENT_VERSION).zip .
	zip -g "./.package/nops-aws-forwarder-deployment-package-$(CURRENT_VERSION).zip" *.py
	rm -rf venv

test:
	rm -rf venv
	python3 -m venv venv
	. venv/bin/activate; pip install -r requirements.txt -r requirements.dev.txt; pytest
	rm -rf venv

environment:
	python3 -m venv env
	. env/bin/activate; pip install -r requirements.txt -r requirements.dev.txt; 
