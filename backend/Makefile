# Define the Python virtual environment directory
VENV := venv
PYTHON := python3
ACTIVATE := source $(VENV)/bin/activate
PWD := $(shell pwd)
.PHONY: venv clean

venv:
	$(PYTHON) -m venv $(VENV)

install: venv
	$(ACTIVATE) && pip install -r requirements.txt

run: install
	$(ACTIVATE) && uvicorn lambda_api.app:app --reload

# deploy changes that require dependency updates.
full-clean-deploy: clean docker-install copy-files install deploy

# deploy changes to code (won't update dependencies)
deploy: copy-files
	$(ACTIVATE) && cdk deploy

# install python requirements that are compatible with AWS Lambda architecture
docker-install:
	docker run --rm -v $(PWD)/lambda_api:/lambda_api -w /lambda_api amazonlinux:latest \
    bash -c "yum install -y python3-pip && pip3 install -r requirements.txt -t package/"
	docker run --rm -v $(PWD)/lambda_import_exhibitions:/lambda_import_exhibitions -w /lambda_import_exhibitions amazonlinux:latest \
    bash -c "yum install -y python3-pip && pip3 install -r requirements.txt -t package/"
	docker run --rm -v $(PWD)/lambda_import_weather:/lambda_import_weather -w /lambda_import_weather amazonlinux:latest \
    bash -c "yum install -y python3-pip && pip3 install -r requirements.txt -t package/"

# copy lambda code and shared modules to package directories for later use by CDK.
copy-files:
	mkdir -p lambda_api/package/backend
	cp lambda_api/app.py lambda_api/package/app.py
	cp settings.py lambda_api/package/settings.py
	cp model.py lambda_api/package/model.py
	
	mkdir -p lambda_import_exhibitions/package/backend/
	cp lambda_import_exhibitions/lambda_function.py lambda_import_exhibitions/package/lambda_function.py
	cp settings.py lambda_import_exhibitions/package/backend/settings.py
	cp model.py lambda_import_exhibitions/package/backend/model.py

	mkdir -p lambda_import_weather/package/backend/
	cp lambda_import_weather/lambda_function.py lambda_import_weather/package/lambda_function.py
	cp settings.py lambda_import_weather/package/backend/settings.py
	cp model.py lambda_import_weather/package/backend/model.py

clean:
	rm -rf $(VENV)
	rm -rf lambda_api/package
	rm -rf lambda_import_weather/package
	rm -rf lambda_import_exhibitions/package
	