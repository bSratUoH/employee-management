import json
import uuid
from datetime import datetime
from botocore.exceptions import ClientError
from utils.clients import table

def lambda_handler(event, context):
    try:
        # taking requested data in request body
        request_body = json.loads(event['body'])
        

        # this function will check the all required keys
        validateEmployeeData(request_body, include_regid=False)
        
        # Check for duplicate email
        email = request_body['email']
        response = table.get_item(Key={'email': email})
        if 'Item' in response:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Employee already exists',
                    'success': False
                })
            }
        
        # to get unique employee id
        regid = generate_employee_id()
        request_body['regid'] = regid
        table.put_item(Item=request_body)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Employee created successfully',
                'regid': regid,
                'success': True
            })
        }
        
    # Bad request response
    except ValueError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': str(e),
                'success': False
            })
        }
    
    # Exception handling for DynamoDB errors
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Employee creation failed',
                'success': False
            })
        }
        
    # exception handling for code break
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f'Employee creation failed: {e}',
                'success': False
            })
        }

def validateEmployeeData(request_body, include_regid=False):
    '''
    this function will check all the required keys to store a employee details 
    and Validate data types based on the provided specifications
    '''
    
    required_keys = ['name', 'email', 'age', 'gender', 'phoneNo', 'addressDetails',
                        'workExperience', 'qualifications', 'projects', 'photo']
    
    # Include 'regid' as a required key
    if include_regid:
        required_keys.append('regid')
        
    # to check all parameter is persent or not
    for key in required_keys:
        if key not in request_body:
            raise ValueError("invalid body request parameter is missing")
    
    data_types = {'name': str, 'email': str, 'age': int, 'gender': str, 'phoneNo': str, 'addressDetails': dict,
                'workExperience': list, 'qualifications': list, 'projects': list, 'photo': str }
    # to validate datatype of parameter
    for key, data_type in data_types.items():
        if key in request_body and not isinstance(request_body[key], data_type):
            raise ValueError("Invalid data type")
        
        
def generate_employee_id():
    # Generate a unique employee ID using UUID4
    return "emp{}".format(str(uuid.uuid4()))