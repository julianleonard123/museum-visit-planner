
Technology Choices:
* Python program language:
 - I am familiar with it.
 - It was mentioned on the job description as a programming language used by Artmyn.
 - I chose to use Python 3.12 since it's a stable supported version and should support any libraries, frameworks I choose to use later.
 - I also choose to use pyenv to manage my Python version and virtual environments to better control my dev environment so that I can commit my code to a GitHub repo and allow other Engineers to pull my code and get started quickly.
 - I considered using `make` file for easy reptition of common commands.

 * AWS
 - I am familiar with it, and it's one of the leading public cloud service providers, with multiple easy to use native services that will address the compute, storage, network requirements of my project.


 * Infrastructure as Code
 - I could have set up an AWS environment manually via the AWS console, but in practice that's not scalable, repeatable, secure enough for a production environment.
 - I also wanted to try out CDK since that's a popular Infrastructure as code technology that I've heard of but not used in the past (and it was mentioned as being used by Artmyn.)  I've use vanilla CloudFormation, Serverless framework and some homegrown tools at other companies to provision AWS infrastructure.


* I took some time to learn CDK - found a good Youtube video giving me an introduction.  https://www.youtube.com/watch?v=D4Asp5g4fp8

* Using my own AWS Free tier account, I deployed one of the existing

AI assistants:
* Use Amazon Q (AI coding assistant)
* Chat GPT
* Warp terminal - built in AI assistant.


CDK:

One stack, one app for now... could separate out into multiple stacks in future... but for ease of deployment initially will use jsut one stack in one app.

I use 1Password to manage my AWS credential, which also supports the cdk.

I bootstrapped my cdk environment with this command:
```
cdk bootstrap aws://247411243287/eu-central-1
```


Looked at an article (albeit from 2020) that used Django, Fargate and CDK.  It looks involved for a time bound case study but I could remove some of the parts I don't need.  But here are some of things I think I could use.

Django
Docker
Vue.js

SQLite - since that's included with Python.

Deploy docker via:
Elastic Bean Stalk
ECS?
Fargate?
EKS?

First, an API that integrates Harvard Art
Museums data and weather forecasts with a caching layer.

Second, a frontend application
that helps art enthusiasts make weather-informed decisions about their weekend plans.

In interest of time...

Implement a Step Function using CDK that calls a:

Python lambda to retrieve Harvard info and write to DynamoDB.

Python lambda to retreive city list from DynamoDB and make calls to 

Implement a Fast API lambda to read from DynamoDB.

Implement front end in React and then

Use AWS Amplify to host the Web app.


Provision a user in my AWS account with Admin access