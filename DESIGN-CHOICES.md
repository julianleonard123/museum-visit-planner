

Design decisions / Trade offs / Shortcuts.

# Architecture / Framework choices

## Backend Architecture 

For this project I decided to use a couple of managed AWS services for compute (AWS Lambda) and storage (DynamoDB).  AWS Lambda is a convenient way to run smaller, discrete functions like the `ImportExhbitions` and `ImportWeather` on a schedule (using Event Bridge Rules).  AWS Lambda means I don't have to manage servers (e.g. Ec2) or a Kubernetes deployment for a project that will have lower usage.  

I chose to use the FastAPI framwork for the API Lambda that serves the results from DynamoDB.  I like this framework as it makes it easy to build an API and comes with automatically generated API docs, which makes sharing detail about the API easy with other team members.

## Trade Offs

Latency for cold starts on API calls:  AWS Lambda works great for async type processes (like the scheduled import lambdas) where slower load times are not noticeable for end users.  However, using a Python Lambda to serve API requests can cause noticeable latency on cold starts.  For an API with a steady flow of requests this cold start will be observed infrequently as AWS recycles Lambda runtime environments.  For lower throughput APIs the cold starts will make up a higher proportion of requests leading to higher overrall latencies.  However, the ease of deployment and lack of servers to manage makes this trade off tolerable. 

## Frontend Architecture

I chose to use AWS Amplify to deploy a frontend application.  This AWS service takes care of integrating with GitHub, deploying application assets, hosting the assets and configuring dns entries.  This is similar to what is offered by Vercel, but I have used AWS Amplify before so I knew it could be set up quickly.

I chose to use a React + Vite template to get started with the front end, since I've done a project using React in the past and this is one of the templates supported by AWS Amplify.  This template was straightforward to get working locally.

After I got a working version of the frontend connecting to the backend I added `tailwind` css to improve the look and feel of the app.

# Automating the Deploy

The `frontend` part of the application has a nice setup thanks to AWS Amplify which is configured to deploy any changes pushed to the `main` branch of the GitHub repo.  Would like to set up additional branch deploys, so I can test without impacting the main version of the application.

The `backend` components were deployed directly from my terminal using CDK.  In a real environment I'd use something like Jenkins to manage a more repeatable process i.e. when a PR request is opened, do a clean deploy of the Stack, and run a suite of end to end tests, invoking the backend API and exercising the UI with a testing framework like Cypress. I really liked the experience of using CDK, it's a better developer experience than using CloudFormation and Serverless framework.

## Better Packaging of Lambda dependencies

I had to do a couple of of hacky things to get the Python dependencies packaged for deployment e.g. I had some target platform issues for the FastAPI dependencies, to I used a docker `amazonlinux` to install versions that are compatible with Lambda runtime.  I also had to revert the Python runtime to 3.9 to get things to play nice, but I know 3.9 is getting old now.. With a bit more time I would figure out which specific dependencies were casuing the issues and explore cleaner ways to package dependencies e.g. using a Lambda Layer.

In previous projects I used some [serverless framework](https://www.serverless.com/) plugins to handle Python dependencies, but this was my first time using CDK so I am sure there is a cleaner way to do this.  These workarounds can be seen in the `Makefile` commands for docker install and file copies.

# Testing

Some basic unit testing included, but ideally would add more integration type tests e.g. run `amazon/dynamodb-local`.  Would also use completely separate stacks for a `stage` version of the application.


# Production Readiness

Error Handling - no custom error handling, api will return Internal Server error for all errors.
Proper logging - instead of basic print statements.

# Use of AI Tools

I used VS Code as my IDE for this project, and I use the AWS Toolkit extension, which includes Amazon Q, with is Amazon's AI assistant.  I find it quite useful for code suggeestions for Python functions and especially handy for writing Python unit tests.

I also used ChatGPT for help getting started with frameworks I was just learning (e.g. CDK and tailwind css).  It also helped me work through various error messages (e.g. I had a CDK boostrap when issue deploying the backend app alongside the AWS Amplify frontend, as it was using another version of the CDK toolkit stack, and ChatGPT helped me solve this problem. )

# Database Access Patterns / Scale

Shortcut: I used a scan request to retrieve all items from the database at once. I kept the number of items in the database small by requesting just the `current` exhibitions from the Harvard API.  At higher scale I'd need to change this to a query that can page through a larger number of results.  The Fast API Lambda would also need to support paging and allowing for server side filtering by weather, which is only a client side filter now.

Shortcut: the items in the database don't ever expire - I would add TTL to remove the items from the database some time after the exhibition has passed, to prevent unnecessary growth of database.


# Additional Functionality

With more time I would route new route to the application on frontend and backend to see details for an individual exhibition.

