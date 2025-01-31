# Museum Visit Planner

Welcome to the Museum Visit Planner (named since this is an MVP minimal viable product :) ).   This application will let you plan a trip to a museum exhibition, including weather forecast information for the exhibition location.

Deployed frontend: [link](https://main.d1e551jiip3ocv.amplifyapp.com/)

Deployed backend API spec: [link](https://onunlky5ka.execute-api.eu-central-1.amazonaws.com/prod/)

This repo contains two projects:

1. A serverless `backend` application, written in Python, that includes:
      1. An AWS Lambda to retrieve Exhbition data from the [Harvard Art Museum API](https://api.harvardartmuseums.org/") and store in DynamoDB.
      2. An AWS Lambda to retrieve weather data for each Exhbitiion venue from [Open Meteo](https://open-meteo.com/), and enrich the items in DynamoDB.
      3. An AWS Lambda running FastAPI to expose rest based API, via an AWS API Gateway.

2. A `frontend` application, written using React + Vite template, that queries the Rest API backend.

# Archictecture Diagram
![Architecture Diagram](/MVP.png)


# Technologies Used

1. Backend: Cloud Native Services
    1. AWS Lambda
    2. AWS DynamoDB (via boto3 client)
    3. AWS Api Gateway
    4. AWS Secrets Manager
2. Infrastructure as Code
    1. AWS CDK
3. Frontend:
    1. React + Vite
    2. AWS Amplify for deployment and hosting

# Developer Environment Setup

## Prerequisites
1. An AWS Account with credentials configured locally.
2. `aws cli` installed locally [link](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).
3. Python installed locally (recommend using [pyenv](https://github.com/pyenv/)).
3. `Node` v22 installed locally (recommend using [nvm](https://github.com/nvm-sh/nvm)).
4. CDK installed locally [link](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html).


## Manual Steps in AWS console (could be automated with more time)
1. Create a Secret for the Harvard Art Museum API key to avoid committing it to GitHub.
2. Set up AWS Amplify to deploy frontend app on push to main branch in GitHub repo. Follow the steps [here](https://aws.amazon.com/getting-started/hands-on/build-react-app-amplify-graphql/module-one/)
3. Create an IAM User for credentials to use when pushing from CDK locally.

## Quick Instructions

### Backend
Build and deploy the `backend` using the Makefile commands, found in the `backend` directory.

Run the FastAPI locally
```
make run
```

Deploy to AWS using CDK
```
make full-clean-deploy
```

Clean up
``` 
make clean
```

### Frontend

Run locally, in `frontend` directory:
```
npm run dev
```

### Detailed instructions


Note: this instructions are for mac os local environment.

#### Pyenv Install
```
  brew update
  brew install pyenv
```
Configure pyenv for your choice of terminal 
e.g. for ksh
```
  echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
  echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
  echo 'eval "$(pyenv init - zsh)"' >> ~/.zshrc
```


Use pyenv to download 3.12 version of Python.
```
pyenv install 3.12
``` 

Set this version of Python to be used:
```
pyenv local 3.12
```

Check that it's set
```
python --version
```
should output something like:
```
julianleonard@Julians-Laptop  museum-visit-planner % python --version
Python 3.12.8
```

To use CDK you will need to install Node.  I recommend using `nvm` (https://github.com/nvm-sh/nvm) to install and manage your node version (similar to `pyenv` above).  For this case study I am using node `v.22.11.0`.

#### CDK Install Instructions
Also, this readme assumes you have an AWS account and the `aws cli` installed already: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

Install the CDK:
```
npm install -g aws-cdk
```
Check the version that is installed:
```
(myenv) julianleonard@Julians-Laptop  museum-visit-planner % cdk version
2.177.0 (build b396961)
```

### Boostrap your CDK environment

If you working in an AWS environment which has not been bootstrapped for CDK, you'll need to run this command: `cdk bootstrap aws://<aws-account-id>/<region>` e.g.
```
cdk bootstrap aws://1234567890/eu-central-1
```