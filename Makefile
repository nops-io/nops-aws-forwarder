package:
	rm -rf venv
	python3 -m venv venv
	. venv/bin/activate; pip install -r requirements.txt
	cd venv/lib/python3.9/site-packages; zip -r ../../../../nops-aws-forwarder-deployment-package.zip .
	zip -g nops-aws-forwarder-deployment-package.zip *.py
	rm -rf venv


test:
	rm -rf venv
	python3 -m venv venv
	. venv/bin/activate; pip install -r requirements.txt -r requirements.dev.txt; pytest
	rm -rf venv

environment:
	python3 -m venv env
	. env/bin/activate; pip install -r requirements.txt -r requirements.dev.txt; 
