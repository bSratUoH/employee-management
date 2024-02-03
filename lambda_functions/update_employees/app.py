import json
from botocore.exceptions import ClientError
from lambda_functions.create_employees.app import validateEmployeeData
from utils.clients import table


def lambda_handler(event, context):
    """Sample pure Lambda function"""

    try:
        # taking requested data in request body
        request_body = json.loads(event['body'])
        
        # Validate data types and required keys
        validateEmployeeData(request_body, include_regid=True)
        
        # Check if employee with regid exists
        regid = request_body['regid']
        response = table.get_item(Key={'regid': regid})
        if 'Item' not in response:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'No employee found with this regid',
                    'success': False
                })
            }
            
    # Bad request response
    except ValueError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'Invalid body request: ' + str(e),
                'success': False
            })
        }
    
    # Exception handling for DynamoDB errors
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Employee updation failed: ' + str(e),
                'success': False
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f'Employee creation failed: {e}',
                'success': False
            })
        }