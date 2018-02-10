# FizzBuzz As A Service

A fully buzzword-compliant FizzBuzz solution for the modern enterprise.

In today's rapidly changing cyber landscape, fizzing buzzes on-site simply isn't agile enough to maintain your competitive advantage.
Ask your developer if FZBZaaS is right for you.


Try it out:
- [/fizzbuzz?data=1,2,3,4,5,6,7,15](https://i564e9ob81.execute-api.us-east-1.amazonaws.com/prod/fizzbuzz?data=1,2,3,4,5,6,7,15)
- [/fizzbuzz?data=2](https://i564e9ob81.execute-api.us-east-1.amazonaws.com/prod/fizzbuzz?data=2)

## Dependencies
This is an HTTP microservice that was written in Python 2.7. 
It is designed to run on [AWS Lambda](https://aws.amazon.com/lambda/)
and be triggered by [API Gateway](https://aws.amazon.com/api-gateway/).
I used [python-lambda](https://github.com/nficano/python-lambda) to simplify deployment.

## Input format
The service expects GET requests with query parameter data set to a comma separated list of one or more integers:
`/fizzbuzz?data=1,2,3`

## Output format
For every argument that can be converted to an integer, we output it and the result of FizzBuzzing it.
Input is repeated in the output because it allows us to silently ignore invalid inputs without causing problems for clients.

```JSON
[
   {
      "in": 15,
      "out": "FizzBuzz"
   },
   {
      "in": 10,
      "out": "Buzz"
   }
]
```


## Deployment Instructions

1. Follow the "Getting Started" section of the [python-lambda README file](https://github.com/nficano/python-lambda/blob/master/README.rst), but stop right before running `lambda init`.

2. Copy `config.example.yaml` to `config.yaml`. Then replace the placeholder credentials in `config.yaml` with the `access key id` and `secret access key` associated with an IAM account that is allowed to create and execute lambda functions.
3. Run `lambda deploy` and go get some coffee. It'll take a few minutes.
4. Once you can see your function in the management console, follow the "Wiring to an API endpoint" section of the [python-lambda README file](https://github.com/nficano/python-lambda/blob/master/README.rst).

## Test locally
```bash
mv event.example.json event.json
lambda invoke -v
```


## Issues you might run into when working with Lambda, API Gateway, and python-lambda

* The example code in the python-lambda README will not work for real HTTP requests. It is written as though the body of your request will be passed directly to the Lambda's `event` parameter, but it's actually nested inside of it. Real events will look like this:

  Request:
  ```http
  POST /endpoint?data=15
  {
  	"field1": "value1"
  }
  ```
  Event:

  ```json
  {
    "httpMethod": "POST",
    "body": "{\"field1\": \"value1\"}"
    "queryStringParameters": {
      "data": "15"
    }
  }
  ```
* The README also doesn't cover CORS, which is fine if you don't want to let random websites access your API. Fortunately, CORS is *way* easier to set up in API Gateway than it used to be. Just hit the "Enable CORS" button in the API Gateway console and then add the following to your response headers:
  ```
  Access-Control-Allow-Credentials: true
  Access-Control-Allow-Headers: Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token
  Access-Control-Allow-Origin: *
  ```

* The automatic API Gateway/Lambda integration setup will allow all HTTP methods (GET, POST, OPTIONS, PATCH, etc). You can tinker with API Gateway to only allow the ones you want (in my case, GET and OPTIONS). I like the idea of killing bad requests before they even touch my code, but if you do this, by default, requests with the wrong method will get this response:
  ```
  HTTP/1.1 403 Forbidden
  {"message":"Missing Authentication Token"}
  ```
  rather than a more helpful `405 Method Not Allowed`. This behavior is not standard HTTP, but it is common in AWS APIs because permission to see if a thing exists is separate from permission to view it. You can handle this in your Lambda function by checking `event['httpMethod']`, or you can use API Gateway:
  * Create new ANY method
  * Under "Integration Request", set integration type to "Mock"
  * Under "Method Response", delete the default entry, and add a response with the status code 405.
  * Under "Integration Response", delete the default entry, and add an integration response with "Method response status" set to 405. You can  customize the body of the response in the "Body Mapping Templates" section.
