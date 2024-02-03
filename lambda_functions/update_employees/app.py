import json
from botocore.exceptions import ClientError
from lambda_functions.create_employees.app import validateEmployeeData
from utils.ddbHelper import DDBHelper

ddbHelperObj = DDBHelper()


def lambda_handler(event, context):
    """Lambda function to update an employee detail"""

    try:
        # taking requested data in request body
        request_body = json.loads(event['body'])
        
        # Validate data types and required keys
        validateEmployeeData(request_body, include_regid=True)
        
        # Check if employee with regid exists
        regId = request_body['regid']
        resp = ddbHelperObj.getItem(pk=regId)

        if 'Item' not in resp:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'No employee found with the given details',
                    'success': False
                })
            }
        
        else:
            print(request_body)
            ddbHelperObj.updateItem(request_body)
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Detail updated',
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