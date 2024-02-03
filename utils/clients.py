import boto3


#creating DynamoDB clint 
dynamodb = boto3.resource('dynamodb')
table_name = 'employee'
table = dynamodb.Table(table_name)