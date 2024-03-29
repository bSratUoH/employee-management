import simplejson as json
from botocore.exceptions import ClientError
from utilities.utils import getEmployeeId, lambdaExceptionWrapper
from utilities.ddbHelper import DDBHelper

# creting object of DynamoDB
ddbHelperObj = DDBHelper()


@lambdaExceptionWrapper()
def lambda_handler(event, context):
    """
    this function will take the request bodyThis function will receive the request body, 
    validate its contents, and then incorporate the employee information into the system 
    """
    # taking requested data in request body
    reqBody = json.loads(event['body'])
    
    # Check if employee already exists
    email = reqBody['email']
    resp = ddbHelperObj.queryDDB(email)

    if resp.get("Items"):
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Employee already exists',
                'success': False
            })
        }
    
    # to get unique employee id
    regId = getEmployeeId()
    reqBody['regId'] = regId
    resp = ddbHelperObj.putItem(reqBody)
    
    return {
        'statusCode': 201,
        'body': json.dumps({
            'message': 'Employee created successfully',
            'regId': regId,
            'success': True
        })
    }