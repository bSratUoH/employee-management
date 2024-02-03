import json
from utils.clients import table
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    """Sample pure Lambda function"""
    try:
        # Extract regid from the query parameters
        regid = event.get('queryStringParameters', {}).get('regid')

        if regid:
            # Retrieve a single employee by regid
            response = table.query(
                KeyConditionExpression=Key('regid').eq(regid)
            )

            if response.get('Items'):
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        "message": "Employee details found",
                        "success": True,
                        "employees": response['Items']
                    })
                }
            else:
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        "message": "Employee details not found",
                        "success": False,
                        "employees": []
                    })
                }
        else:
            # Retrieve all employees
            response = table.scan()

            if response.get('Items'):
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        "message": "Employee details found",
                        "success": True,
                        "employees": response['Items']
                    })
                }
            else:
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        "message": "Employee details not found",
                        "success": False,
                        "employees": []
                    })
                }
    except Exception as e:
        return {
            'statusCode': 200,
            'body': json.dumps({
                "message": f"Error: {str(e)}",
                "success": False,
                "employees": []
            })
        }