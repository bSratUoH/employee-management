# Employee Management

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. It includes the following folders.

- lambda_funtions - The code for the Lambda functions in the application includes four functions: one for creating employees, another for updating employee information, one for deleting employees, and one for retrieving employee details.
- lambda_layer/utilities - In this section, I've defined functions for connecting to DynamoDB, establishing client connections, and managing logging.
- samconfig.toml - this file is used to store configuration settings for our SAM projects.
template.yaml - A template that defines the application's AWS resources.

The application uses several AWS resources, including Lambda functions and an API Gateway API. These resources are defined in the `template.yaml` file in this project.

The request validation has also been done using AWS API Gateway Models and can be found inside template.yaml.


## Deploy this application

This application can be deployed using the SAM CLI, you need the following tools.

* SAM CLI.
* Python (3.9)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build
sam deploy --s3-bucket s3-bucket-name
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, the zipped code will be stored in the given s3 bucket.


You can find your API Gateway Endpoint URL in the output values displayed after deployment.


## Features can be improved-

- Authentication for the APIs
- Pagination while fetching employees list
- Separate the template for different resouces and import them in main template
